run:
	docker compose --profile local up --force-recreate

run-rebuild:
	docker compose --profile local up --build