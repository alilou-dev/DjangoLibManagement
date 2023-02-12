.PHONY: migrations build stop restart

migrations:
	docker compose exec web python3 manage.py migrate

build:
	docker-compose -up -d --build

start:
	docker-compose up -d

stop:
	docker-compose down --remove-orphans --volumes --timeout 0

restart: stop start