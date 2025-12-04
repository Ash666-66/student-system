.PHONY: help install dev-install format lint test run clean migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  dev-install  - Install development dependencies with uv"
	@echo "  format       - Format code with ruff and black"
	@echo "  lint         - Lint code with ruff"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  run          - Start development server"
	@echo "  migrate      - Run database migrations"
	@echo "  makemigrations - Create migration files"
	@echo "  superuser    - Create superuser"
	@echo "  clean        - Clean up cache and compiled files"
	@echo "  collectstatic - Collect static files for production"

# Installation
install:
	pip install -r requirements.txt

dev-install:
	uv sync --dev

# Code quality
format:
	uv run ruff format .
	uv run black .

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov=.

# Development commands
run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

superuser:
	uv run python manage.py createsuperuser

# Production commands
collectstatic:
	uv run python manage.py collectstatic --noinput

# Cleanup
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/

# Database reset (use with caution!)
reset-db:
	@echo "⚠️  This will delete all data in the database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	rm -f db.sqlite3
	$(MAKE) migrate
	$(MAKE) superuser