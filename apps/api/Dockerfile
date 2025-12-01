FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY apps/api/ .

# Expose the port
EXPOSE 8000

# Command to run the application
# Command to run the application using the PORT environment variable provided by Railway
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
