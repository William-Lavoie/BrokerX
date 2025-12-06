#!/bin/bash
set -euo pipefail

ALL_SERVICES=("client" "wallet" "stock" "order" "portfolio")

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
    SERVICES=("${ALL_SERVICES[@]}")
fi

if ! docker network ls | grep -q brokerx-network; then
    docker network create brokerx-network
fi

echo "Deploying API Gateway..."
cd gateway
docker compose down -v --remove-orphans > /dev/null 2>&1
docker compose build --no-cache > /dev/null 2>&1
docker compose up -d > /dev/null 2>&1
echo -e "\033[0;32mAPI Gateway deployed successfully.\033[0m"

cd ".."
cd "kafka"
echo "Deploying Kafka..."
docker compose down -v --remove-orphans > /dev/null 2>&1
docker compose build --no-cache > /dev/null 2>&1
docker compose up -d > /dev/null 2>&1
echo -e "\033[0;32mKafka deployed successfully.\033[0m"
cd ".."

for SERVICE in "${SERVICES[@]}"; do
    echo "Deploying $SERVICE..."

    cd "${SERVICE}_service"
    docker compose down -v --remove-orphans > /dev/null 2>&1
    docker compose build --no-cache > /dev/null 2>&1
    docker compose up -d > /dev/null 2>&1
    until docker compose exec -T mysql mysqladmin ping -h "${SERVICE}-mysql" --silent; do
        sleep 2
    done

    echo -e "\033[0;32m$SERVICE deployed successfully.\033[0m"
    cd ".."
done

echo "Cleaning up unused Docker resources..."
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
