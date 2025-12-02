# Runbook for BrokerX

## Overview
This runbook provides operational procedures and troubleshooting steps for managing BrokerX.

##  Starting with Docker
### Starting with `deploy.sh` script
1. To start the service, begin by cloning the Github repository `https://github.com/William-Lavoie/BrokerX` or downloading the source code.
2. Run `BrokerX/deploy.sh`
3. The frontend application should now be running on port 3000 (`http://localhost:3000/`)

### Starting manually
If you prefer not to use the script or it does not work, you can follow these steps.
1. To start the service, begin by cloning the Github repository.
2. Go to each service individually (gateway, kafka, stock_service, order_service, portfolio_service, stock_service, notifications_service, wallet_service and client_service).
3. Run `docker compose down -v` (or `docker compose down` if you want previous data to persist)
4. Run `docker compose build`
5. Run `docker compose up` (or `docker compose up -d` if you want it running in the background)
6. Go to `react_frontend`
7. Run `npm run dev`
8. The frontend should be running at `http://localhost:3000/` with all services available.

Alternatively, choose only the services you want deployed.

### Using the VM
Note that the `deploy.sh` script is automatically called on the VM in the CD script. You can access
the application at `http://10.194.32.208:8000/`.

## Diagnosticating errors
Errors are automatically logged in the `django.error_logs` file, alternatively you can use the command
`docker logs -f broker_app` or `docker logs -f broker_mysql` to access the docker logs.

## Accessing the database
You can access the MySQL command line as root for a particular service by running the following command:
`docker exec -it service-mysql mysql -u root -p`

Where service is replaced by the service for which you wish to access the database.

## Running tests
You can run the tests by running the command
`docker exec {service}_service-{service}-app-1 python -m pytest`, or if you wish to get the coverage
`docker exec {service}_service-{service}-app-1 python -m pytest --cov=broker --cov-config=.coveragerc --cov-report=term-missing`

Where `{service}` is replaced by the name of the service. For example, docker exec order_service-order-app-1 python -m pytest