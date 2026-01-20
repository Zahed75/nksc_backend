#!/bin/bash
# /www/wwwroot/nksc_backend/start.sh
set -e

echo "Starting Django application..."

# Wait for MySQL to be fully ready
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h"nksc-mysql" -u"root" -p"Nksc@2026" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 3
done

echo "MySQL is up and running!"

# Wait a bit more for MySQL to be fully initialized
sleep 5

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if not exists (optional - for first setup)
echo "Checking for superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    nksc_backend.wsgi:application