# Backend - Books App

This is the backend service for the Books App, built with FastAPI and Celery.

## Features
- FastAPI for RESTful APIs
- Celery for background tasks
- SQL Server/MySQL support
- JWT Authentication
- Docker & docker-compose support

## Project Structure
```
backend/
  main.py                # FastAPI entrypoint
  celery_temp/           # Celery worker and tasks
  config/                # Configuration files
  database/              # Database connection modules
  middleware/            # Custom middleware (e.g., auth)
  models/                # SQLAlchemy models
  routes/                # API route definitions
  schemas/               # Pydantic schemas
  services/              # Business logic, utils, response, etc.
  requirements.txt       # Python dependencies
  Dockerfile             # Docker build file
  docker-compose.yml     # Docker Compose config
```

## Local Development
```sh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run with Docker
```sh
docker build -t books-backend .
docker run -p 8000:8000 books-backend
```

## Run with Docker Compose (from project root)
```sh
docker-compose up --build
```

## Celery Worker
```sh
celery -A celery_temp.celery_worker.celery_app worker --loglevel=info
```

## Environment Variables


## License
MIT
