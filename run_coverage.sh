#!/usr/bin/env bash
set -e

echo "📊 Calculating code coverage for wpipe-mcp..."

# Execute pytest with pytest-cov to calculate coverage metrics
PYTHONPATH=src pytest --cov=src/wpipe_mcp tests/ --cov-report=term-missing --cov-report=html

echo "✅ Coverage report generated. View HTML report at htmlcov/index.html"
