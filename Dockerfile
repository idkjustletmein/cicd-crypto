# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and apply security patches
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "jaraco.context>=6.1.0" "wheel>=0.46.2"

# Copy the project code into the container
COPY . .

# Collect static files and create media dir
RUN python manage.py collectstatic --noinput || true
RUN mkdir -p /app/media/key_files

# Expose the port the app runs on
EXPOSE 8000

# Run migrations and start the server
CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000
