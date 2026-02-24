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

# Expose the port the app runs on
EXPOSE 8000

# Run the application
# Using 0.0.0.0 to make it accessible outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
