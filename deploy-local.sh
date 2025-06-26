#!/bin/bash

# Build and start containers
docker-compose up -d --build

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations for each service
docker-compose exec auth-service python manage.py migrate
docker-compose exec destination-service python manage.py migrate
docker-compose exec comment-service python manage.py migrate
docker-compose exec like-service python manage.py migrate

# Create superuser for auth service
docker-compose exec auth-service python manage.py createsuperuser

echo "Deployment completed successfully!" 