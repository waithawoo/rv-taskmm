#!/bin/bash
set -e

echo "Starting quick-start for RV-TASKMM..."

if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Python is not installed."
    exit 1
fi

# --- Step 1: Root environment (.env) ---
if [ ! -f .env ]; then
    echo "Copying root .env..."
    cp .env.example .env
else
    echo "Root .env exists, skipping."
fi

# --- Step 2: Backend environment (.env) ---
echo "Generating backend .env..."
$PYTHON backend/src/tools/core/cli.py generate:env

# --- Step 3: Frontend environment (.env) ---
if [ ! -f frontend/.env ]; then
    echo "Copying frontend .env..."
    cp frontend/.env.example frontend/.env
else
    echo "Frontend .env exists, skipping."
fi

# --- Step 4: Build & start all Docker services ---
echo "Building and starting Docker services..."
docker compose up -d --build

sleep 5

# --- Step 5: Run DB migrations ---
echo "Running database migrations..."
docker exec -it wtotaskmm_backend python src/tools/db/cli.py migrate

# --- Step 6: Seed database with sample data ---
echo "Seeding database..."
docker exec -it wtotaskmm_backend python src/tools/db/cli.py seed

# --- Step 7: Run backend tests ---
read -p "Do you want to run backend tests? (y/N): " run_backend_tests
if [[ "$run_backend_tests" =~ ^[Yy]$ ]]; then
    echo "Running backend tests..."
    docker exec -it wtotaskmm_backend pytest src/tests -v
fi

# --- Step 8: Run frontend tests ---
read -p "Do you want to run frontend tests? (y/N): " run_frontend_tests
if [[ "$run_frontend_tests" =~ ^[Yy]$ ]]; then
    echo "Running frontend tests..."
    cd frontend
    npm install
    npm test
    cd ..
fi

echo "✅ Quick-start finished!"
