SERVICE=api
CONTAINER=vin-python-monolith-api-1

.PHONY: init
init:
	$(MAKE) build
	$(MAKE) up
	$(MAKE) migrate

.PHONY: migrate
migrate:
	docker-compose run --rm $(SERVICE) alembic upgrade head

.PHONY: up
up:
	docker-compose up -d

.PHONY: build
build:
	docker-compose build