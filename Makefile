DOCKER_COMPOSE ?= docker-compose

all: compose

COMPOSE_FILE_NAME ?= docker-compose.yml
COMPOSE_FILE_NAME_DEV ?= docker-compose.dev.yml

compose: compose-down compose-up
compose-dev: compose-down-dev compose-up-dev

compose-up:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_NAME) up -d --build --force-recreate
compose-down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_NAME) down -v

compose-up-dev:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_NAME_DEV) up -d --build --force-recreate
compose-down-dev:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_NAME_DEV) down -v

createsuperuser:
	docker exec -it portald python3 manage.py createsuperuser

migrate:
	docker exec -it portald python3 manage.py makemigrations
	docker exec -it portald python3 manage.py migrate
