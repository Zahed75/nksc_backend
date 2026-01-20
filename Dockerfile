# Dockerfile - COLLECT STATIC DURING BUILD
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Set proper permissions (RUN as root, so we have permission)
RUN chown -R 1000:1000 /app && \
    chmod -R 755 /app

# Create non-root user
RUN useradd -m -u 1000 django

# Switch to non-root user
USER django

# Collect static files during build (as root, then fix permissions)
USER root
RUN python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."
RUN chown -R django:django /app/staticfiles
USER django

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "nksc_backend.wsgi:application"]