.ONESHELL:

run-dev:
	docker compose down
	docker compose build 
	docker compose up

run-production:
	docker compose up
