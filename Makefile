# Makefile

SHELL := /bin/bash

-include src/.env
export

install_all_deps:
	poetry install --with=tests,develop

run_api_worker:
	poetry run python src/api_entrypoint.py --reload

run_lint:
	poetry run python -m isort . && poetry run python -m flake8 src/ tests/ --extend-ignore=ASYNC9,ASYNC102,ASYNC120

# создать миграции
makemigration:
	@read -p "Migration title: " migration_title; \
	cd src; \
	poetry run alembic revision --autogenerate -m "$$migration_title"

# применить миграции
migrate:
	@cd src; \
	poetry run alembic upgrade head

# откатить последнюю миграцию
downgrade:
	@cd src; \
	poetry run alembic downgrade -1

# создать миграции
show_migration:
	@read -p "Destination revision id or revision_from:revision_to: " revision; \
	cd src; \
	poetry run alembic upgrade --sql "$$revision"

run_tests:
	poetry run python -m pytest ./tests --disable-warnings

build_openapi_documentation:
	@cd src/; \
	poetry run python -m extract_openapi
