import os
import sys
import argparse
import subprocess
import signal
import json
import logging
from mcp.server.fastmcp import FastMCP
from wpipe_mcp.catalog import StepsCatalog
from wpipe_mcp.templates import TemplateGenerator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# PID file for background service
PID_FILE = os.path.expanduser("~/.wpipe_mcp.pid")

# Create the primary FastMCP Server instance
mcp = FastMCP("wpipe-mcp-server")
catalog = StepsCatalog()

# --- Tools ---

@mcp.tool()
def search_wpipe_step(query: str) -> str:
    """Search for existing pipeline steps in official and community catalogs."""
    results = catalog.search(query)
    if not results:
        return f"No custom step matching '{query}' was found. Recommend building a native WPipe Class-based Step."
    
    response = "Found production-ready architectural steps in wisrovi SUITE:\n\n"
    for s in results:
        response += f"🚀 [{s.get('origin', 'Unknown')}] {s.get('func_name', s.get('label'))}\n"
        response += f"   - Description: {s.get('description', 'N/A')}\n"
        response += f"   - Namespace: {s.get('namespace', 'N/A')}\n\n"
    return response

@mcp.tool()
def deploy_wpipe_scaffolding(target_dir: str, project_name: str = "wpipe_project", pipeline_type: str = "standard") -> str:
    """Deploys a professional WPipe project structure with class-based states."""
    try:
        if not os.path.isabs(target_dir):
            return "Error: target_dir must be an absolute path."

        for folder in TemplateGenerator.get_folders(pipeline_type):
            os.makedirs(os.path.join(target_dir, folder), exist_ok=True)

        blueprints = TemplateGenerator.get_files_blueprint(pipeline_type, project_name)
        for rel_path, content in blueprints.items():
            full_path = os.path.join(target_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return f"Success: WPipe architecture '{project_name}' deployed at {target_dir}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_wpipe_architect_manual() -> str:
    """Expert manual for building high-performance pipelines (wisrovi standard)."""
    return (
        "WPIPE ARCHITECT MANUAL\n"
        "1. Prefer Class-based States (@step).\n"
        "2. Use Typed Context (PipelineContext/Pydantic).\n"
        "3. Apply @to_obj on __call__.\n"
        "4. Always use tracking_db for forensics."
    )

# --- CLI Actions ---

def run_stdio():
    """Runs the MCP server in stdio mode (standard for agents)."""
    mcp.run(transport="stdio")

def run_sse():
    """Runs the MCP server in SSE mode."""
    mcp.run(transport="sse")

def start_background():
    """Starts the SSE server in the background."""
    if os.path.exists(PID_FILE):
        print("Server is already running or PID file exists.")
        return

    # In a real scenario, we would use a proper daemon library, 
    # but for simplicity, we use subprocess.
    proc = subprocess.Popen(
        [sys.executable, "-m", "wpipe_mcp.server", "run-sse"],
        stdout=open(os.path.expanduser("~/wpipe_mcp.log"), "a"),
        stderr=subprocess.STDOUT,
        preexec_fn=os.setpgrp
    )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))
    print(f"wpipe-mcp started in background (SSE mode) with PID {proc.pid}")

def stop_background():
    """Stops the background SSE server."""
    if not os.path.exists(PID_FILE):
        print("No background server running.")
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read())
    
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped server with PID {pid}")
    except ProcessLookupError:
        print("Process not found.")
    finally:
        os.remove(PID_FILE)

def print_config():
    """Prints the JSON configuration for agents."""
    path = subprocess.check_output(["which", "wpipe-mcp"]).decode().strip()
    config = {
        "mcpServers": {
            "wpipe-mcp": {
                "command": path,
                "args": ["run"],
                "env": {}
            }
        }
    }
    print(json.dumps(config, indent=2))

# --- Main Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="wpipe-mcp: WPipe Architect MCP Server")
    parser.add_argument("command", nargs="?", default="run", 
                        choices=["run", "run-sse", "start", "stop", "config", "help"],
                        help="Command to execute (default: run)")

    args = parser.parse_args()

    if args.command == "run":
        run_stdio()
    elif args.command == "run-sse":
        run_sse()
    elif args.command == "start":
        start_background()
    elif args.command == "stop":
        stop_background()
    elif args.command == "config":
        print_config()
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
