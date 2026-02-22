SHELL := /bin/bash

.PHONY: help up down logs fmt lint test

help:
	@echo "Targets:"
	@echo "  up    - docker compose up --build"
	@echo "  down  - docker compose down -v"
	@echo "  logs  - docker compose logs -f"
	@echo "  fmt   - (placeholder) format python (ruff/black) if installed"
	@echo "  lint  - (placeholder) lint python (ruff) if installed"
	@echo "  test  - run pytest in services/aib-api"

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	cd services/aib-api && python -m pytest -q
