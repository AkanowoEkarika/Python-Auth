# Auth Service

A Django REST API for user registration, JWT login, and password reset using Redis. Configured for PostgreSQL and Render deployment.

## Requirements

- Python 3.11+
- PostgreSQL 14+
- Redis 6+

## Setup

1. Create virtualenv and install deps:
   - Windows (PowerShell):
     - `py -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
     - `pip install -r requirements.txt`
   - Linux/macOS:
     - `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

2. Create `.env` at project root based on `.env.example`.

3. Run migrations and start server:
   - `python manage.py migrate`
   - `python manage.py runserver`

## Environment variables

- `SECRET_KEY` (required in production)
- `DEBUG` (default: `False`)
- `ALLOWED_HOSTS` (comma separated, default: `*`)
- `DATABASE_URL` (e.g., `postgres://user:pass@host:5432/dbname`)
- `REDIS_URL` (e.g., `redis://:password@host:6379/1`)

## API Endpoints

- `POST /api/auth/register/` { full_name, email, password }
- `POST /api/auth/token/` { username=email, password }
- `POST /api/auth/token/refresh/` { refresh }
- `POST /api/auth/forgot-password/` { email }
- `POST /api/auth/reset-password/` { token, new_password }
- `GET /api/docs/` Swagger UI

## Tests

- `python manage.py test`

## Deployment (Render)

- Use `render.yaml` to provision web service and PostgreSQL/Redis.
- `Dockerfile` builds image with Gunicorn + WhiteNoise.
- Set environment variables in Render dashboard or via `render.yaml`.
