.ONESHELL:

run-dev:
	docker compose down
	docker compose build

	: > logs/django.log
	docker compose up

run-production:
	docker compose up
