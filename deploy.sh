#!/bin/bash
set -euo pipefail

SERVICES=("client_service" "wallet_service", "order_service")

git reset --hard
git pull origin main
git clean -fd

docker network rm brokerx-network > /dev/null || true

for SERVICE in "${SERVICES[@]}"; do
    echo "Deploying $SERVICE..."

    cd "$SERVICE"
    docker compose down -v --remove-orphans
    docker compose build --no-cache
    docker compose up -d

    echo "$SERVICE deployed successfully."
    cd "..."
done
cd ".."

docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f
docker builder prune -af

echo "All services deployed successfully."

echo "Deploying frontend"
cd "react_frontend"
npm install
npm run dev
echo "BrokerX is available at http://localhost:3000"
