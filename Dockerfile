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

# Python Dependencies (minimal for production)
COPY requirements-minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8080

# Start with debug entrypoint
CMD ["./entrypoint.sh"]
