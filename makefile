.ONESHELL:

clean:
	: > logs/django.log
	find storage -mindepth 1 ! -name '.gitignore' -delete

run-dev: clean
	docker compose down
	docker compose build
	docker compose up

run-production:
	docker compose down
	docker compose build
	docker compose up -d

test-e2e:
	docker compose exec django python manage.py test tests.e2e

clean-db:
	docker compose exec django python manage.py clean_db

restart-django:
	docker compose restart django

restart-redis:
	docker compose restart redis

restart-mongodb:
	docker compose restart horizon-mongodb

restart-celery-worker:
	docker compose restart celery-worker

restart-celery-beat:
	docker compose restart celery-beat
