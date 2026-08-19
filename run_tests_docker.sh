#!/usr/bin/env bash
set -e

echo "🐳 Running wpipe-mcp unit tests inside a Docker container..."

# Run test suite using a python:3.11-slim image mounting the current repository
docker run --rm \
  -v "$(pwd)":/usr/src/app \
  -w /usr/src/app \
  python:3.11-slim \
  bash -c "pip install --no-cache-dir -e '.[dev]' && PYTHONPATH=src pytest tests/ -v"

echo "✅ Dockerized test suite completed successfully."
