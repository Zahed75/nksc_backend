# Dockerfile - FIXED PERMISSIONS
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories with proper permissions BEFORE switching user
RUN mkdir -p /app/media /app/staticfiles /app/logs && \
    chown -R 1000:1000 /app && \
    chmod -R 755 /app

# Create non-root user
RUN useradd -m -u 1000 django

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Run Gunicorn directly (remove collectstatic from command)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "nksc_backend.wsgi:application"]