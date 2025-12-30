# Makefile for LoL AI Coach
# Session 8: PostgreSQL Migration

.PHONY: health check test dev

# System health check (Session 8)
health:
	@python3 scripts/check_system.py

# Alias for health
check: health

# Run development server
dev:
	@echo "Starting development server..."
	@uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# Run tests (TODO: implement pytest suite)
test:
	@echo "Running tests..."
	@pytest tests/ -v

# Help
help:
	@echo "Available commands:"
	@echo "  make health  - Run system health check"
	@echo "  make check   - Alias for health"
	@echo "  make dev     - Start development server"
	@echo "  make test    - Run test suite"
