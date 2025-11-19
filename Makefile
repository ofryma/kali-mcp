.PHONY: setup install test test-unit test-integration test-coverage run stop clean help

setup:
	python -m venv .venv
	@source .venv/bin/activate
	@pip install -r requirements.txt

install: setup

# Run all tests
test:
	pytest

# Run unit tests only
test-unit:
	pytest -m "not integration" -v

# Run integration tests only
test-integration:
	pytest -m integration -v

# Run tests with coverage report
test-coverage:
	pytest --cov=server --cov=kali_server --cov-report=html --cov-report=term

# Run tests in watch mode
test-watch:
	pytest-watch

# Run specific test file
test-file:
	pytest $(FILE) -v

run:
	@docker-compose -f "MCP-Kali-Server/docker-compose.yml" up -d
	@python "MCP-Kali-Server/mcp_http_server.py"

stop:
	docker-compose -f "MCP-Kali-Server/docker-compose.yml" down

# Clean up test artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Show help
help:
	@echo "Available targets:"
	@echo "  setup              - Install dependencies"
	@echo "  test               - Run all tests"
	@echo "  test-unit          - Run unit tests only"
	@echo "  test-integration   - Run integration tests only"
	@echo "  test-coverage      - Run tests with coverage report"
	@echo "  test-watch         - Run tests in watch mode"
	@echo "  test-file FILE=... - Run specific test file"
	@echo "  run                - Start the server"
	@echo "  stop               - Stop the server"
	@echo "  clean              - Clean up test artifacts"
	@echo "  help               - Show this help message"
