#!/bin/bash

# Build and start services in detached mode
docker-compose up -d --build

echo "Services started in background. To view logs use: docker-compose logs -f"
echo "To stop services use: docker-compose down" 