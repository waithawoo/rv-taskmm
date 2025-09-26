FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \ 
    libmariadb3 libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    libsasl2-dev \
    python3-dev \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*
    
COPY ./requirements/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT
ENV PORT=$PORT

CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:$PORT --reload --log-level info"]
