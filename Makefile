DOCKER_COMPOSE = docker-compose -f docker-compose.yml
DRUN = $(DOCKER_COMPOSE) run --rm

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down
