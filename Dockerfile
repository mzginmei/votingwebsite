FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=website.settings

WORKDIR /app

# System deps (optional but common for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

# Ensure the expected STATIC/MEDIA paths exist inside the image
RUN mkdir -p /home/web/dsa/static /home/web/dsa/media

# Collect static at build time
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

EXPOSE 8080

# For simple deployments; consider gunicorn for production later.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]