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

.PHONY: api
api:
	docker exec -it vin-python-monolith-api-1 bash

.PHONY: logs
logs:
	docker exec -it ${CONTAINER} tail -f logs/app.log