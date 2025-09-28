#!/bin/bash
set -euo pipefail

# Pull code
git reset --hard
git pull origin main
git clean -fd

# Start Docker containers
docker compose stop
docker compose down -v
docker compose build --no-cache
docker compose up -d --remove-orphans

# Cleanup docker ressources
docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f
docker builder prune -af

echo "Deployment completed successfully."
echo "BrokerX is available on port 8000"
