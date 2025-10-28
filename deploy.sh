#!/bin/bash
set -euo pipefail

SERVICES=("client_service" "wallet_service", "order_service")

git stash >/dev/null 2>&1
git checkout main >/dev/null 2>&1
git reset --hard >/dev/null 2>&1
git pull origin main >/dev/null 2>&1
git clean -fd >/dev/null 2>&1

docker network rm brokerx-network >/dev/null 2>&1 || true

for SERVICE in "${SERVICES[@]}"; do
    echo "Deploying $SERVICE..."

    cd "$SERVICE"
    docker compose down -v --remove-orphans
    docker compose build --no-cache
    docker compose up -d

    echo "\033[0;32m$SERVICE deployed successfully.\033[0;32m"
    cd ".."
done
cd ".."

docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f
docker builder prune -af

echo "\033[0;32mAll services deployed successfully.\033[0;32m"

echo "Deploying frontend"
cd "react_frontend"
npm install
npm run dev
echo "BrokerX is available at http://localhost:3000"
