# 🦅 wpipe-mcp

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/wisrovi/wpipe-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-1.0-orange.svg)](https://modelcontextprotocol.io)

**Transform your AI Agents into expert WPipe Architects.**

`wpipe-mcp` is a professional Model Context Protocol (MCP) server that bridges the gap between AI Agents (Claude, Gemini, OpenCode) and the **wisrovi SUITE**. It empowers agents to search, design, validate, and deploy high-performance pipelines following strict industry-standard patterns.

---

## ✨ Key Features

- **🔍 Expert Catalog Search**: Query over 100+ production-ready steps from Official and Community registries.
- **🏗️ Strict Architecture Enforcement**: Guides AI to output clean code using mandatory `dto/`, `states/`, and `main.py` folder structures, including the new internal microservice `app/` layout.
- **🛡️ Project Architectural Validation**: Verify that any existing code structure complies with the WPipe standards using `validate_wpipe_project` to check directories, step decorators, and context schemas.
- **📘 Architect's Manual**: Built-in expertise for Monolith-to-Pipeline refactoring, performance tracking, and resilient state management.
- **💻 Unified CLI**: Manage your MCP service with simple commands: `run`, `start`, `stop`, and `config`.
- **🔒 Privacy First**: 100% local execution via `stdio` or `SSE`.

---

## 🛠️ Key Technologies & Libraries

This MCP server relies on the following key tools and libraries:
* **Model Context Protocol (MCP)**: Server protocol implementation for agent interaction.
* **FastMCP (mcp-sdk-python)**: Framework to declare tools and resources cleanly.
* **Pydantic**: Structural validation, schema checks, and context enforcement.
* **Pytest & Pytest-Cov**: Automated unit testing and coverage report analysis.
* **Ruff**: Modern linting and styling consistency.

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and run the automated installer, or install via pip:
```bash
pip install -e .
```

### 2. Integration
Get your agent-specific configuration block and installation commands by running:
```bash
wpipe-mcp config
```
The CLI will dynamically detect your Python environment and provide exact copy-paste commands for Gemini CLI (e.g. `gemini mcp add ...`) and JSON blocks for Claude Desktop.

---

## 🧪 Running Tests

Unit tests are written with `pytest`. You can run them in three ways:

### 1. Locally (with development dependencies installed)
To execute tests locally with python path environment set up:
```bash
PYTHONPATH=src pytest tests/ -v
```

### 2. Inside a Docker Container (Recommended)
To run tests in a containerized environment to isolate dependencies:
```bash
./run_tests_docker.sh
```

### 3. Calculate Code Coverage
To run tests and get a detailed statement of code coverage:
```bash
./run_coverage.sh
```
This generates an HTML report in `htmlcov/index.html`.

---

## 📂 Project Structure
- `src/wpipe_mcp/`: Core server logic and tools.
- `src/wpipe_mcp/catalog.py`: Real-time GitHub catalog synchronization.
- `src/wpipe_mcp/templates.py`: Professional boilerplate definitions.
- `examples/`: Sample implementations and use cases.
- `tests/`: Automated unit tests verifying blueprints, scaffolding, and validation.

---

## 📄 License
MIT License - Crafted with ❤️ by **William Rodriguez** (wisrovi).
