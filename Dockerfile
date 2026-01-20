# Dockerfile - FIXED GUNICORN
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/django/.local/bin:${PATH}"

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

# Install gunicorn explicitly
RUN pip install --no-cache-dir gunicorn

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/media /app/staticfiles /app/logs && \
    chown -R 1000:1000 /app && \
    chmod -R 755 /app

# Create non-root user
RUN useradd -m -u 1000 django

# Switch to non-root user
USER django

# Add user's local bin to PATH
ENV PATH="/home/django/.local/bin:${PATH}"

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "nksc_backend.wsgi:application"]