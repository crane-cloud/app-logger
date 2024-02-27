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



# set default target
.DEFAULT_GOAL := help

# colors
YELLOW := $(shell tput -Txterm setaf 3)
NC := "\e[0m"

#shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE