# Dockerfile for Railway Deployment
# ==================================
# Version: 2.0 - Clean deployment without PORT variables

FROM python:3.11-slim

# Working Directory
WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start application (Railway provides $PORT)
# Use shell form to allow environment variable expansion
CMD ["sh", "-c", "uvicorn api_v2:app --host 0.0.0.0 --port ${PORT:-8080}"]
