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

# Setup logging strictly to stderr to avoid breaking MCP protocol
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# PID file for background service
PID_FILE = os.path.expanduser("~/.wpipe_mcp.pid")

# Create the primary FastMCP Server instance
mcp = FastMCP("wpipe-mcp-server")
catalog = None # Lazy initialization

def get_catalog():
    global catalog
    if catalog is None:
        catalog = StepsCatalog()
    return catalog

# --- Tools ---

@mcp.tool()
def get_wpipe_architect_blueprints() -> str:
    """Provides expert code blueprints for high-performance WPipe States and Pipelines."""
    state_code = (
        "from wpipe import step, to_obj\\n"
        "from wpipe.timeout import timeout_sync\\n"
        "from typing import Any\\n"
        "from pydantic import BaseModel\\n\\n"
        "class MyContext(BaseModel):\\n"
        "    field: str\\n\\n"
        "@step(\\n"
        "    name=\"MyStep\",\\n"
        "    version=\"v1.0\",\\n"
        "    timeout=10,\\n"
        "    description=\"Step description\",\\n"
        "    tags=[\"custom\"],\\n"
        "    retry_count=3,\\n"
        "    retry_delay=0.01,\\n"
        ")\\n"
        "class MyStep:\\n"
        "    def __init__(self, config: str = \"value\"):\\n"
        "        self.config = config\\n\\n"
        "    @timeout_sync(seconds=2)\\n"
        "    @to_obj(MyContext)\\n"
        "    def __call__(self, context: Any) -> Any:\\n"
        "        # Professional logic here\\n"
        "        print(f\"🚀 Executing with config: {self.config}\")\\n"
        "        return context\\n"
    )
    
    pipeline_code = (
        "from wdecorators import time_execution\\n"
        "from wpipe import Pipeline, ResourceMonitor, TaskTimer\\n"
        "from wpipe.exception.api_error import ProcessError\\n\\n"
        "def run_pipeline():\\n"
        "    pipeline = Pipeline(\\n"
        "        pipeline_name=\"professional_pipeline\",\\n"
        "        pipeline_version=\"1.0.0\",\\n"
        "        tracking_db=\"output/tracking.db\",\\n"
        "        collect_system_metrics=True,\\n"
        "        show_progress=True,\\n"
        "        max_retries=3,\\n"
        "        retry_delay=0.5\\n"
        "    )\\n\\n"
        "    pipeline.set_steps([step_1])\\n\\n"
        "    if __name__ == \"__main__\":\\n"
        "        try:\\n"
        "            with ResourceMonitor(\"my_monitor\") as monitor:\\n"
        "                with TaskTimer(\"my_timer\", timeout_seconds=900) as timer:\\n"
        "                    @time_execution\\n"
        "                    def run():\\n"
        "                        return pipeline.run({{\"data\": \"init\"}})\\n"
        "                    run()\\n"
        "            summary = monitor.get_summary()\\n"
        "            print(f\"Peak RAM: {summary['peak_ram_mb']} MB\")\\n"
        "        except ProcessError as e:\\n"
        "            print(f\"Error: {e}\")\\n"
    )
    
    return (
        "WPIPE EXPERT BLUEPRINTS\\n\\n"
        "### 1. Advanced State Pattern:\\n" + state_code + "\\n\\n"
        "### 2. High-Performance Pipeline Pattern:\\n" + pipeline_code
    )

@mcp.tool()
def search_wpipe_step(query: str) -> str:
    """Search for existing pipeline steps in official and community catalogs."""
    results = get_catalog().search(query)
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
        "WPIPE ARCHITECT MANUAL (ADVANCED)\n"
        "1. Prefer Class-based States (@step) for complex logic.\n"
        "2. Contexts must inherit from pydantic.BaseModel for strong typing.\n"
        "3. Use @timeout_sync(seconds=N) and @to_obj(ContextClass) on __call__.\n"
        "4. Always use tracking_db=\"path/to/db\" for forensics and metrics.\n"
        "5. Wrap execution in ResourceMonitor and TaskTimer context managers.\n"
        "6. Use @time_execution decorator from wdecorators for performance tracking.\n"
        "7. Configure max_retries and retry_delay at both Step and Pipeline levels."
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

def print_config(write_file: bool = True):
    """Prints or saves the JSON configuration for agents."""
    python_path = sys.executable
    config = {
        "mcpServers": {
            "wpipe-mcp": {
                "command": python_path,
                "args": ["-m", "wpipe_mcp.server", "run"],
                "env": {}
            }
        }
    }

    config_json = json.dumps(config, indent=2)

    if not write_file:
        print(config_json)
        return

    # Create .agents directory in the current working directory
    target_dir = os.getcwd()
    agents_dir = os.path.join(target_dir, ".agents")
    os.makedirs(agents_dir, exist_ok=True)
    
    config_path = os.path.join(agents_dir, "wpipe-mcp.json")
    with open(config_path, "w") as f:
        f.write(config_json)
    
    print(f"✅ Configuration saved to: {config_path}")

# --- Main Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="wpipe-mcp: WPipe Architect MCP Server")
    parser.add_argument("command", nargs="?", default="run", 
                        choices=["run", "run-sse", "start", "stop", "config", "help"],
                        help="Command to execute (default: run)")
    parser.add_argument("--print", action="store_true", 
                        help="Print configuration to stdout instead of saving to .agents/")

    args = parser.parse_args()

    # Silence logging for 'config' to keep output clean
    if args.command == "config":
        logging.getLogger().setLevel(logging.ERROR)
        print_config(write_file=not args.print)
        return


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
