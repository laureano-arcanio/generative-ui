run:
	docker compose --profile local up --force-recreate

run-rebuild:
	docker compose --profile local up --build

db-migrate:
	docker compose exec backend poetry run alembic upgrade head

generate-migration:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Migration name is required. Use 'make generate-migration \"<migration name>\"'"; \
		exit 1; \
	fi
	docker compose exec backend poetry run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"