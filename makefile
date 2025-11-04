.ONESHELL:

run-dev:
	docker compose down
	docker compose build

	: > logs/django.log
	docker compose up

run-production:
	docker compose up

test-e2e:
	docker compose exec django python manage.py test tests.e2e