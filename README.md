# 🦅 wpipe-mcp

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/wisrovi/wpipe-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-1.0-orange.svg)](https://modelcontextprotocol.io)

**Transform your AI Agents into expert WPipe Architects.**

`wpipe-mcp` is a professional Model Context Protocol (MCP) server that bridges the gap between AI Agents (Claude, Gemini, OpenCode) and the **wisrovi SUITE**. It empowers agents to search, design, and deploy high-performance pipelines following strict industry-standard patterns.

---

## ✨ Key Features

- **🔍 Expert Catalog Search**: Query over 100+ production-ready steps from Official and Community registries.
- **🏗️ Strict Architecture Enforcement**: Guides AI to output clean code using mandatory `dto/`, `states/`, and `main.py` folder structures.
- **📘 Architect's Manual**: Built-in expertise for Monolith-to-Pipeline refactoring, performance tracking, and resilient state management.
- **💻 Unified CLI**: Manage your MCP service with simple commands: `run`, `start`, `stop`, and `config`.
- **🛡️ Privacy First**: 100% local execution via `stdio` or `SSE`.

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

## 🛠️ CLI Usage

| Command | Description |
| :--- | :--- |
| `wpipe-mcp run` | Start the server in `stdio` mode (default for agents). |
| `wpipe-mcp start` | Start as an SSE server in the background. |
| `wpipe-mcp stop` | Stop the background server. |
| `wpipe-mcp config` | Generate and save JSON config to `.agents/wpipe-mcp.json`. |
| `wpipe-mcp config --print` | Show JSON configuration in stdout (no file creation). |
| `wpipe-mcp help` | Show available tools and commands. |

---

## 📂 Project Structure
- `src/wpipe_mcp/`: Core server logic and tools.
- `src/wpipe_mcp/catalog.py`: Real-time GitHub catalog synchronization.
- `src/wpipe_mcp/templates.py`: Professional boilerplate definitions.
- `examples/`: Sample implementations and use cases.

---

## 📄 License
MIT License - Crafted with ❤️ by **William Rodriguez** (wisrovi).
