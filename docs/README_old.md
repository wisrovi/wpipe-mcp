# wpipe-mcp 🦅

An advanced Model Context Protocol (MCP) local-first server designed to empower AI Agents (Claude Desktop, Gemini CLI, OpenCode) with the capacity to autonomously architect, search, and deploy high-performance workflows using the **wisrovi SUITE**.

---

## 🛡️ Architecture & Privacy (Local-First Design)

Following strict infrastructure hardening and privacy standards, this server operates entirely on the client-side using **Standard Input/Output (stdio) communication channels**. No external network sockets are opened, making it highly secure and fully transparent for corporate compliance.

---

## 🚀 Installation & Agent Setup

### 1. Install the Local Package
Clone this repository locally and install it using pip:
```bash
pip install .
```

### 2. Configure Your AI Agent

Add the server declaration to your agent's configuration file (e.g., claude_desktop_config.json):

```json
{
  "mcpServers": {
    "wpipe-mcp-server": {
      "command": "wpipe-mcp",
      "args": [],
      "env": {}
    }
  }
}
```


### 🛠️ Exposed AI Tools

search_wpipe_step: Queries the live or cached components catalog to find reuseable solutions from nearly 100 modules in wpipe_steps.

deploy_wpipe_scaffolding: Safely builds and populates the production-ready directory layout for ETL pipelines or MLOps architectures (wtrain + wyolo) directly onto the client's storage.


