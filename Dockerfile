# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

RUN python -c "open('Procfile','w').write('web: gunicorn auth_service.wsgi --bind 0.0.0.0:$PORT')"

CMD ["bash", "-lc", "python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn auth_service.wsgi --bind 0.0.0.0:$PORT"]
