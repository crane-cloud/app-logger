DOCKER_DEV_COMPOSE_FILE := docker-compose.yml


help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build-image: ## Build docker image
	@ ${INFO} "Building required docker images"
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) build app-logger
	@ ${INFO} "Image succesfully built"
	@ echo " "

start:build-image ## Start server
	@ ${INFO} "starting local development server"
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) up

connect-to-container:build-image ## Connect to a container
	@ ${INFO} "Connecting to a container"
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) exec app-logger /bin/bash

build-testing-image: ## Build docker image
	@ ${INFO} "Building testing docker images"
	@ docker network inspect cranecloud_default >/dev/null 2>&1 || docker network create cranecloud_default
	@ export FASTAPI_ENV='testing' 
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) build --build-arg FASTAPI_ENV=testing app-logger 
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) up -d app-logger logger-celery-worker logger-mongo-db logger-redis-db
	@ sleep 2 
	@ ${INFO} "Image succesfully built"
	@ echo " "

test:build-testing-image ## Run tests
	@ ${INFO} "Running tests"
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) exec app-logger  poetry run pytest --cov=. --cov-report=term-missing
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) stop app-logger logger-celery-worker logger-mongo-db logger-redis-db 


clean: ## Remove all project images and volumes
	@ ${INFO} "Cleaning your local environment"
	@ ${INFO} "Note: All ephemeral volumes will be destroyed"
	@ docker compose -f $(DOCKER_DEV_COMPOSE_FILE) down --rmi all
	@ ${INFO} "Clean complete"

# set default target
.DEFAULT_GOAL := help

# colors
YELLOW := $(shell tput -Txterm setaf 3)
NC := "\e[0m"

#shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE