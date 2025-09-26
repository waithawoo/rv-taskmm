# Task Managment project assignment documentation

## Stack and Architecture Overview

### Backend

- Framework: FastAPI (Python 3.12+)
- Database: MySQL 8.0 with SQLAlchemy ORM
- Cache: Redis 7 for token blocklist
- Authentication: JWT tokens with refresh token mechanism
- API Documentation: OpenAPI/Swagger with automatic generation
- Testing: Pytest with async support

### Frontend

- Framework: Next.js 15.5.3 with React 19
- Styling: Tailwind CSS 4.0
- State Management: React Context API
- HTTP Client: Native fetch API
- Testing: Jest with React Testing Library
- Development: Turbopack for fast builds

### Infrastructure

- Containerization: Docker with Docker Compose
- Database: MySQL with persistent volumes
- Networking: Bridge network for service communication

## REST API

### Authentication

- use JWT with Refresh Tokens
  - Access tokens: Short-lived (60 minutes) for security
  - Refresh tokens: Long-lived (7 days) for convenience
  - Token blocklist in Redis for immediate logout
- implement CORS settings
- implement Redis based ratelimiting

Considering the furture case for mobile devices, JWT json is returned in FastAPI backend instead of httponly cookie response.
But in Nextjs, not to expose jwt in browser storage, proxy apis are used with httponly cookie for jwt tokens.
The overview flow will be as follow.

- Browser submits login -> hits Next.js API route (/api/login) -> no JWT exposure.
- Next.js server calls actual FastAPI /api/v1/auth/login internally. FastAPI returns JWT in JSON.
- Next.js stores JWT server-side with HttpOnly cookie for the browser.
- Browser never sees the raw JWT -> it only has an HttpOnly cookie.
- All subsequent requests go through Next.js API routes which attaches JWT, to FastAPI requests.

### Pagination

Cursor-based pagination is implmented.

- `cursor` and `limit` including other filter like sort, search etc.
- Response includes `next_cursor`, `has_next` to know next page
- Cursor is base64 encoded string.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.12+ (for local development)

#### 1. Quick start

- run ./quick-start.sh (from env config, db seed to running test cases)

```bash
chmod +x quick-start.sh
./quick-start.sh
```

#### 2. Comprehensive start (Please read and do as folows)

##### ENV configuration

- Clone the repo and setup .env files for root (docker compose), backend and frontend.
- Set up the `.env` file for the root path (used by Docker Compose), backedn and frontend.
- For local testing, it is ok enough to use default values from .env.example

```bash
git clone https://github.com/waithawoo/rv-taskmm.git

cd rv-taskmm

# For Root environment
cp .env.example .env

# For Backend environment
python backend/src/tools/core/cli.py generate:env

# For Frontend environment
cp frontend/.env.example frontend/.env
```

##### Start and Database Setup

```bash
# Start all services
docker compose up -d --build

# Run database migrations
docker exec -it wtotaskmm_backend python src/tools/db/cli.py migrate

# Seed database with sample data
docker exec -it wtotaskmm_backend python src/tools/db/cli.py seed
```

##### Testing

- Backend tests can be run in docker container.

```bash
docker exec -it wtotaskmm_backend pytest src/tests -v 
```

- Fronted tests can be run in local normal mode.

```bash
cd frontend && npm install && npm test
```

## API Documentation

The interactive API documentation can be checked as followed.

- Swagger UI: <http://localhost:8000/doc/api-doc>

## Demo URL

I have also deployed to server. So the demo url will be

- Main URL will be <https://demo1.waithawoo.com>
- API Documentation will be <https://demo1.waithawoo.com/doc/api-doc>

## Sample User Accounts to test for both local and demo server

```bash
Admin account
email - admin@gmail.com
password - password

User accounts
email - userone@gmail.com
password - password

email - usertwo@gmail.com
password - password
```
