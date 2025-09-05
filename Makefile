# Makefile for Geo-fence Alert Service

.PHONY: help install dev test lint clean docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  test        - Run tests with coverage"
	@echo "  lint        - Run code linting"
	@echo "  clean       - Clean up cache and temp files"
	@echo "  docker-build- Build Docker image"
	@echo "  docker-up   - Start services with Docker Compose"
	@echo "  docker-down - Stop Docker Compose services"
	@echo "  run         - Run the application locally"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev:
	pip install -r requirements.txt
	pip install -r requirements-test.txt
	pip install black flake8 isort mypy

# Run tests with coverage
test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Run code linting
lint:
	black --check .
	flake8 .
	isort --check-only .
	mypy .

# Format code
format:
	black .
	isort .

# Clean up cache and temp files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Docker operations
docker-build:
	docker build -t geofence-service .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Run the application locally
run:
	python main.py

# Run database migrations
migrate:
	docker-compose exec postgres psql -U geofence_user -d geofence_db -f /docker-entrypoint-initdb.d/sample_data.sql

# Check service health
health:
	curl -f http://localhost:8000/health || exit 1

# Full development setup
setup: install dev docker-up
	@echo "Development environment ready!"
	@echo "Service running at: http://localhost:8000"
	@echo "Database available at: localhost:5432"
	@echo "Redis available at: localhost:6379"