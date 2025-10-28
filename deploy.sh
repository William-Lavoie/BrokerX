#!/bin/bash
set -euo pipefail

ALL_SERVICES=("client_service" "wallet_service" "order_service")

if [ "$#" -gt 0 ]; then
    SERVICES=()
    for s in "$@"; do
        if [[ " ${ALL_SERVICES[*]} " == *" $s "* ]]; then
            SERVICES+=("$s")
        else
            echo -e "\033[0;31mUnknown service: $s\033[0m"
            exit 1
        fi
    done
else
    # No arguments, deploy all services
    SERVICES=("${ALL_SERVICES[@]}")
fi

git stash >/dev/null 2>&1
git reset --hard >/dev/null 2>&1
#git pull origin main >/dev/null 2>&1
git clean -fd >/dev/null 2>&1

if ! docker network ls | grep -q brokerx-network; then
    docker network create brokerx-network
fi
docker network create brokerx-network

for SERVICE in "${SERVICES[@]}"; do
    echo "Deploying $SERVICE..."

    cd "$SERVICE"
    docker compose down -v --remove-orphans
    docker compose build --no-cache
    docker compose up -d
    docker compose run --rm "$SERVICE" python manage.py migrate

    echo -e "\033[0;32m$SERVICE deployed successfully.\033[0m"
    cd ".."
done

echo "Deploying Gateway..."

cd "gateway"
docker compose down -v --remove-orphans
docker compose build --no-cache
docker compose up -d

echo -e "\033[0;32mGateway deployed successfully.\033[0m"
cd ".."

docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f
docker builder prune -af

echo -e "\033[0;32mAll services deployed successfully.\033[0m"

echo "Deploying frontend"
cd "react_frontend"
npm install
npm run dev
echo "BrokerX is available at http://localhost:3000"
