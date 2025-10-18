# Gemini MCP Server Makefile

.PHONY: help install test clean demo server format lint

# Default target
help:
	@echo "🚀 Gemini MCP Server"
	@echo "===================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install dependencies and setup environment"
	@echo "  test       - Run tests"
	@echo "  demo       - Run demo script"
	@echo "  server     - Start MCP server"
	@echo "  format     - Format code with black and isort"
	@echo "  lint       - Run linting checks"
	@echo "  clean      - Clean up temporary files"
	@echo "  dev-install - Install development dependencies"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	python3 -m venv .venv || true
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "✅ Installation complete!"

# Install development dependencies
dev-install:
	@echo "📦 Installing development dependencies..."
	.venv/bin/pip install -r requirements-dev.txt
	@echo "✅ Development installation complete!"

# Run tests
test:
	@echo "🧪 Running tests..."
	.venv/bin/python -m pytest tests/ -v

# Run demo
demo:
	@echo "🎬 Running demo..."
	@if [ -z "$$GEMINI_API_KEY" ]; then \
		echo "❌ Please set GEMINI_API_KEY environment variable"; \
		exit 1; \
	fi
	.venv/bin/python demo.py

# Start MCP server
server:
	@echo "🚀 Starting MCP server..."
	@if [ -z "$$GEMINI_API_KEY" ]; then \
		echo "❌ Please set GEMINI_API_KEY environment variable"; \
		exit 1; \
	fi
	.venv/bin/python run_server.py

# Format code
format:
	@echo "🎨 Formatting code..."
	.venv/bin/black src/ tests/ *.py
	.venv/bin/isort src/ tests/ *.py
	@echo "✅ Code formatted!"

# Run linting
lint:
	@echo "🔍 Running linting..."
	.venv/bin/black --check src/ tests/ *.py
	.venv/bin/isort --check-only src/ tests/ *.py
	@echo "✅ Linting complete!"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Show project status
status:
	@echo "📊 Project Status"
	@echo "================"
	@echo "Python version: $$(python3 --version)"
	@echo "Virtual env: $$(.venv/bin/python --version 2>/dev/null || echo 'Not created')"
	@echo "API Key set: $$([ -n "$$GEMINI_API_KEY" ] && echo 'Yes' || echo 'No')"
	@echo "Dependencies: $$(.venv/bin/pip list 2>/dev/null | wc -l || echo 'Not installed') packages"