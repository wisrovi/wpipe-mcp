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
    level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr
)
logger = logging.getLogger(__name__)

# PID file for background service
PID_FILE = os.path.expanduser("~/.wpipe_mcp.pid")

# Create the primary FastMCP Server instance
mcp = FastMCP("wpipe-mcp-server")
catalog = None  # Lazy initialization


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
        "from wpipe import step, to_obj\n"
        "from wpipe.timeout import timeout_sync\n"
        "from typing import Any\n"
        "from pydantic import BaseModel\n\n"
        "class MyContext(BaseModel):\n"
        "    field: str\n\n"
        "@step(\n"
        '    name="MyStep",\n'
        '    version="v1.0",\n'
        "    timeout=10,\n"
        '    description="Step description",\n'
        '    tags=["custom"],\n'
        "    retry_count=3,\n"
        "    retry_delay=0.01,\n"
        ")\n"
        "class MyStep:\n"
        '    def __init__(self, config: str = "value"):\n'
        "        self.config = config\n\n"
        "    @timeout_sync(seconds=2)\n"
        "    @to_obj(MyContext)\n"
        "    def __call__(self, context: Any) -> Any:\n"
        "        # Professional logic here\n"
        '        print(f"🚀 Executing with config: {self.config}")\n'
        "        return context\n"
    )

    pipeline_code = (
        "from wdecorators import time_execution\n"
        "from wpipe import Pipeline, ResourceMonitor, TaskTimer\n"
        "from wpipe.exception.api_error import ProcessError\n\n"
        "def run_pipeline():\n"
        "    pipeline = Pipeline(\n"
        '        pipeline_name="professional_pipeline",\n'
        '        pipeline_version="1.0.0",\n'
        '        tracking_db="output/tracking.db",\n'
        "        collect_system_metrics=True,\n"
        "        show_progress=True,\n"
        "        max_retries=3,\n"
        "        retry_delay=0.5\n"
        "    )\n\n"
        "    pipeline.set_steps([step_1])\n\n"
        '    if __name__ == "__main__":\n'
        "        try:\n"
        '            with ResourceMonitor("my_monitor") as monitor:\n'
        '                with TaskTimer("my_timer", timeout_seconds=900) as timer:\n'
        "                    @time_execution\n"
        "                    def run():\n"
        '                        return pipeline.run({"data": "init"})\n'
        "                    run()\n"
        "            summary = monitor.get_summary()\n"
        "            print(f\"Peak RAM: {summary['peak_ram_mb']} MB\")\n"
        "        except ProcessError as e:\n"
        '            print(f"Error: {e}")\n'
    )

    return (
        "WPIPE EXPERT BLUEPRINTS\n\n"
        "### 1. Advanced State Pattern:\n" + state_code + "\n\n"
        "### 2. High-Performance Pipeline Pattern:\n" + pipeline_code
    )


@mcp.tool()
def search_wpipe_step(query: str) -> str:
    """Search for existing pipeline steps in official and community catalogs."""
    results = get_catalog().search(query)
    if not results:
        return f"No custom step matching '{query}' was found. Recommend building a native WPipe Class-based Step."

    response = "Found production-ready architectural steps in wisrovi SUITE:\n\n"
    for s in results:
        response += (
            f"🚀 [{s.get('origin', 'Unknown')}] {s.get('func_name', s.get('label'))}\n"
        )
        response += f"   - Description: {s.get('description', 'N/A')}\n"
        response += f"   - Namespace: {s.get('namespace', 'N/A')}\n\n"
    return response


@mcp.tool()
def deploy_wpipe_scaffolding(
    target_dir: str,
    project_name: str = "wpipe_project",
    pipeline_type: str = "standard",
    include_tests: bool = True,
) -> str:
    """Deploys a professional WPipe project structure with class-based states."""
    try:
        if not os.path.isabs(target_dir):
            return "Error: target_dir must be an absolute path."

        for folder in TemplateGenerator.get_folders(pipeline_type):
            os.makedirs(os.path.join(target_dir, folder), exist_ok=True)

        blueprints = TemplateGenerator.get_files_blueprint(
            pipeline_type, project_name, include_tests
        )
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
        "--- PROJECT STRUCTURE RULES (MANDATORY) ---\n"
        "1. DTOs: All Pydantic BaseModel classes (Contexts) MUST be placed inside a `dto/` directory (or `app/dto/` in microservices). Create one file per class (e.g., `dto/my_context.py`).\n"
        "2. STATES: All WPipe Step classes MUST be placed inside a `states/` directory (or `app/states/` in microservices). Create one file per step (e.g., `states/my_step.py`), and populate `states/__init__.py` to export them.\n"
        "3. PIPELINE: The orchestrator script MUST be placed in `main.py` at the root level (or `app/main.py` and `app/pipelines.py` in microservices).\n\n"
        "--- MICROSERVICE INTERNAL STRUCTURE (app/ layout) ---\n"
        "For dockerized microservices, the following internal structure inside the `app/` directory is mandatory:\n"
        "- app/config/: Variable configurations unique to the microservice (config.yaml, settings.py) extending global parameters.\n"
        "- app/dto/: Pydantic BaseModel context schemas guaranteeing strict typing and DAG context validation.\n"
        "- app/model/: Pre-trained models (pt, joblib, onnx) loaded on boot or lazy-loaded.\n"
        "- app/services/: Core heavy processing/inference services decoupled from the state machine.\n"
        "- app/states/: WPipe Step classes (decorated with @step) invoking the services and mutating the Context.\n"
        "- app/test/: pytest unit tests. Note: Always ask the user before generating these test files.\n"
        "- app/utils/: Pure utility helper functions.\n"
        "- app/pipelines.py: Declarative construction and assembly of state machine pipelines/graphs.\n"
        "- app/main.py: Entrypoint starting the event listener, running the pipeline, and outputting/routing results.\n\n"
        "--- CORE RULES ---\n"
        "1. Prefer Class-based States (@step) for complex logic.\n"
        "2. Contexts must inherit from pydantic.BaseModel for strong typing.\n"
        "3. Use @timeout_sync(seconds=N) and @to_obj(ContextClass) on __call__.\n"
        '4. Always use tracking_db="path/to/db" for forensics and metrics.\n'
        "5. Wrap execution in ResourceMonitor and TaskTimer context managers.\n"
        "6. Use @time_execution decorator from wdecorators for performance tracking.\n"
        "7. Configure max_retries and retry_delay at both Step and Pipeline levels.\n\n"
        "--- REFACTORING A MONOLITH TO WPIPE ---\n"
        "When refactoring a monolithic script into a WPipe Pipeline, follow this exact workflow:\n"
        "Step 1: Identify the shared state (variables passed between logical chunks of code). Define a single Pydantic BaseModel (Context) that holds all these variables. Save it in `dto/`.\n"
        "Step 2: Break the monolith into logical, isolated 'Steps'. Each Step should be a class decorated with @step. Save each in `states/`.\n"
        "Step 3: The __call__ method of each Step must accept ONLY the Context object, read what it needs from it, and modify it directly before returning it.\n"
        "Step 4: Create `main.py`, configure the Pipeline object, and pass instances of your Step classes to pipeline.set_steps([...]) in the correct execution order.\n"
        "Step 5: Run the pipeline passing a dictionary that matches the initial required fields of your Pydantic Context.\n"
        "Step 6: Generate a professional, intuitive, and modern `README.md` (in English) documenting what the newly created pipeline does. You MUST include a Mermaid flowchart diagram (`mermaid`) illustrating the pipeline's execution flow and steps. Also, you MUST include a footer or header stating: 'Generated by WPipe MCP by wisrovi'."
    )


@mcp.tool()
def validate_wpipe_project(project_path: str) -> str:
    """Validates if a local project complies with the official WPipe architecture structure (standard or microservice app/ layout)."""
    import re
    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    issues = []
    successes = []
    
    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)

    base_dir = app_dir if is_microservice else project_path
    layout_name = "Microservice app/ layout" if is_microservice else "Standard layout"
    
    main_file = os.path.join(base_dir, "main.py")
    if not os.path.exists(main_file):
        issues.append(f"❌ Missing core entrypoint: 'main.py' not found in {base_dir}.")
    else:
        successes.append(f"✅ Found main entrypoint: 'main.py' in {base_dir}.")

    if is_microservice:
        pipelines_file = os.path.join(base_dir, "pipelines.py")
        if not os.path.exists(pipelines_file):
            issues.append("❌ Missing declarative pipelines assembly: 'pipelines.py' not found in app/.")
        else:
            successes.append("✅ Found declarative pipelines: 'pipelines.py' in app/.")

    required_dirs = ["dto", "states"]
    for d in required_dirs:
        dir_path = os.path.join(base_dir, d)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            issues.append(f"❌ Missing mandatory directory: '{d}/' not found in {base_dir}.")
        else:
            successes.append(f"✅ Found directory: '{d}/' in {base_dir}.")

    if is_microservice:
        optional_dirs = ["config", "model", "services", "utils", "test"]
        for d in optional_dirs:
            dir_path = os.path.join(base_dir, d)
            if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                issues.append(f"⚠️ Recommendation: Optional directory '{d}/' not found in app/.")
            else:
                successes.append(f"✅ Found optional directory: '{d}/' in app/.")

    step_decorator_regex = re.compile(r"@step\s*\(")
    base_model_regex = re.compile(r"class\s+\w+\s*\(\s*BaseModel\s*\)")

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in (".git", ".venv", "venv", "__pycache__", "build", "dist", ".mypy_cache", ".pytest_cache")]
        for file in files:
            if not file.endswith(".py"):
                continue
            
            full_file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(full_file_path, project_path)
            
            try:
                with open(full_file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if step_decorator_regex.search(content):
                    norm_root = os.path.normpath(root)
                    rel_to_base = os.path.relpath(norm_root, base_dir)
                    if rel_to_base.split(os.sep)[0] != "states":
                        issues.append(f"❌ Architectural violation: WPipe '@step' class defined in '{rel_file_path}' outside of the states/ directory.")
                
                if base_model_regex.search(content):
                    norm_root = os.path.normpath(root)
                    rel_to_base = os.path.relpath(norm_root, base_dir)
                    first_part = rel_to_base.split(os.sep)[0]
                    if first_part not in ("dto", "config"):
                        issues.append(f"❌ Architectural violation: Pydantic 'BaseModel' defined in '{rel_file_path}' outside of the dto/ or config/ directory.")
            except Exception:
                pass

    report = "## WPipe Project Architectural Report\n"
    report += f"**Detected Layout:** {layout_name}\n"
    report += f"**Validated Path:** `{project_path}`\n\n"
    
    if issues:
        report += "### 🔴 Compliance Issues & Warnings:\n"
        for issue in issues:
            report += f"- {issue}\n"
        report += "\n"
    else:
        report += "### 🎉 Compliance Status: Fully Compliant\n"
        report += "No architectural violations or missing directories were found!\n\n"

    if successes:
        report += "### 🟢 Verified Components:\n"
        for success in successes:
            report += f"- {success}\n"

    return report


@mcp.tool()
def document_wpipe_project(project_path: str, write_to_readme: bool = True) -> str:
    """Inspects a WPipe project and generates flow charts (Mermaid DAG) and technical documentation tables, writing them to README.md."""
    import re
    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)
    base_dir = app_dir if is_microservice else project_path

    # 1. Discover step metadata by reading files in states/
    states_dir = os.path.join(base_dir, "states")
    steps_metadata = {}
    if os.path.exists(states_dir) and os.path.isdir(states_dir):
        for root, _, files in os.walk(states_dir):
            for file in files:
                if not file.endswith(".py"):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    matches = re.finditer(r"@step\s*\((.*?)\)\s*class\s+(\w+)", content, re.DOTALL)
                    for m in matches:
                        args_str, class_name = m.groups()
                        metadata = {
                            "name": class_name,
                            "version": "1.0",
                            "timeout": "N/A",
                            "description": "N/A",
                            "tags": [],
                            "retry_count": "0",
                            "retry_delay": "0",
                        }
                        
                        for key in ["name", "version", "description"]:
                            arg_match = re.search(rf'{key}\s*=\s*["\'](.*?)["\']', args_str)
                            if arg_match:
                                metadata[key] = arg_match.group(1)
                                
                        timeout_match = re.search(r'timeout\s*=\s*(\d+)', args_str)
                        if timeout_match:
                            metadata["timeout"] = f"{timeout_match.group(1)}s"
                            
                        retry_count_match = re.search(r'retry_count\s*=\s*(\d+)', args_str)
                        if retry_count_match:
                            metadata["retry_count"] = retry_count_match.group(1)
                            
                        retry_delay_match = re.search(r'retry_delay\s*=\s*([\d\.]+)', args_str)
                        if retry_delay_match:
                            metadata["retry_delay"] = f"{retry_delay_match.group(1)}s"
                            
                        tags_match = re.search(r'tags\s*=\s*\[(.*?)\]', args_str, re.DOTALL)
                        if tags_match:
                            tags_content = tags_match.group(1)
                            tags = [t.strip().strip('"').strip("'") for t in tags_content.split(",") if t.strip()]
                            metadata["tags"] = tags
                            
                        steps_metadata[class_name] = metadata
                except Exception:
                    pass

    # 2. Trace step execution order from pipelines.py or main.py
    pipelines_file = os.path.join(base_dir, "pipelines.py")
    if not os.path.exists(pipelines_file):
        pipelines_file = os.path.join(base_dir, "main.py")
        
    ordered_steps = []
    if os.path.exists(pipelines_file):
        try:
            with open(pipelines_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            set_steps_match = re.search(r"set_steps\(\s*\[(.*?)\]\s*\)", content, re.DOTALL)
            if set_steps_match:
                steps_content = set_steps_match.group(1)
                instances = re.findall(r"(\w+)\s*\(", steps_content)
                for inst in instances:
                    if inst in steps_metadata:
                        ordered_steps.append(inst)
                    elif inst.endswith("Step"):
                        ordered_steps.append(inst)
        except Exception:
            pass

    if not ordered_steps:
        ordered_steps = list(steps_metadata.keys())

    # 3. Generate Markdown section
    flow_md = "<!-- WPIPE_FLOW_START -->\n"
    flow_md += "## 🦅 WPipe Execution Flow\n\n"
    
    if ordered_steps:
        flow_md += "### 🔄 DAG Flowchart\n"
        flow_md += "```mermaid\n"
        flow_md += "graph TD\n"
        flow_md += "    Start([Start]) --> Step_0\n"
        for i, step_name in enumerate(ordered_steps):
            meta = steps_metadata.get(step_name, {})
            label = meta.get("name", step_name)
            ver = meta.get("version", "1.0")
            tags = ", ".join(meta.get("tags", []))
            tags_str = f"<br/><i>{tags}</i>" if tags else ""
            flow_md += f'    Step_{i}["{label} (v{ver}){tags_str}"]\n'
            if i > 0:
                flow_md += f"    Step_{i-1} --> Step_{i}\n"
        flow_md += f"    Step_{len(ordered_steps)-1} --> End([End])\n\n"
        flow_md += "    style Start fill:#f3f4f6,stroke:#d1d5db,stroke-width:2px;\n"
        flow_md += "    style End fill:#f3f4f6,stroke:#d1d5db,stroke-width:2px;\n"
        for i, step_name in enumerate(ordered_steps):
            flow_md += f"    style Step_{i} fill:#dbeafe,stroke:#3b82f6,stroke-width:2px;\n"
        flow_md += "```\n\n"
        
        flow_md += "### 📊 Technical Steps Specifications\n"
        flow_md += "| Step Name | Version | Timeout | Retries | Description | Tags |\n"
        flow_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for step_name in ordered_steps:
            meta = steps_metadata.get(step_name, {
                "name": step_name, "version": "1.0", "timeout": "N/A",
                "retry_count": "0", "retry_delay": "0",
                "description": "N/A", "tags": []
            })
            tags = ", ".join([f"`{t}`" for t in meta.get("tags", [])])
            desc = meta.get("description", "N/A")
            retries = f"{meta.get('retry_count')} (delay: {meta.get('retry_delay')})"
            flow_md += f"| `{meta.get('name')}` | {meta.get('version')} | {meta.get('timeout')} | {retries} | {desc} | {tags} |\n"
    else:
        flow_md += "*No active steps or pipelines detected to visualize.*\n"
        
    flow_md += "\n---\n*Generated by WPipe MCP by **wisrovi***\n"
    flow_md += "<!-- WPIPE_FLOW_END -->"

    if write_to_readme:
        readme_path = os.path.join(project_path, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                
                if "<!-- WPIPE_FLOW_START -->" in readme_content and "<!-- WPIPE_FLOW_END -->" in readme_content:
                    pattern = re.compile(r"<!-- WPIPE_FLOW_START -->.*?<!-- WPIPE_FLOW_END -->", re.DOTALL)
                    new_readme = pattern.sub(flow_md, readme_content)
                else:
                    new_readme = readme_content.rstrip() + "\n\n" + flow_md + "\n"
                    
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(new_readme)
            except Exception as e:
                return f"Error writing to README.md: {str(e)}"
        else:
            try:
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(flow_md + "\n")
            except Exception as e:
                return f"Error creating README.md: {str(e)}"

    return f"Success: Technical execution flow documented successfully.\n\n{flow_md}"


@mcp.tool()
def refactor_monolith_to_wpipe(source_file_path: str, target_dir: str) -> str:
    """Refactors a monolithic python script into a clean structured WPipe microservice project layout under target_dir/app/."""
    import ast
    import textwrap
    
    if not os.path.isabs(source_file_path) or not os.path.isabs(target_dir):
        return "Error: Both source_file_path and target_dir must be absolute paths."

    if not os.path.exists(source_file_path):
        return f"Error: Source file '{source_file_path}' does not exist."

    try:
        with open(source_file_path, "r", encoding="utf-8") as f:
            code = f.read()
            f.seek(0)
            lines = f.readlines()
            
        tree = ast.parse(code)
    except Exception as e:
        return f"Error parsing source file: {str(e)}"

    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    
    steps = []
    dto_fields = set()
    
    app_dir = os.path.join(target_dir, "app")
    os.makedirs(os.path.join(app_dir, "dto"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "states"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "config"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "model"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "services"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "utils"), exist_ok=True)
    os.makedirs(os.path.join(app_dir, "test"), exist_ok=True)

    if not functions:
        step_name = "MainProcessStep"
        clean_name = "main_process"
        
        dedented = textwrap.indent(code, "        ")
        step_code = (
            "from typing import Any\n"
            "from wpipe import step, to_obj\n"
            "from dto.context import RefactoredContext\n\n"
            "@step(\n"
            f"    name=\"{step_name}\",\n"
            "    version=\"v1.0\",\n"
            "    timeout=30,\n"
            "    description=\"Auto-refactored step from monolith\",\n"
            ")\n"
            f"class {step_name}:\n"
            "    def __call__(self, context: Any) -> Any:\n"
            "        # Auto-generated step execution logic\n"
            f"{dedented}\n"
            "        return context\n"
        )
        
        steps.append((step_name, clean_name, step_code))
    else:
        for idx, func in enumerate(functions):
            func_name = func.name
            step_name = "".join([part.capitalize() for part in func_name.split("_")]) + "Step"
            clean_name = f"step_{idx}_{func_name}"
            
            args = [arg.arg for arg in func.args.args]
            for arg in args:
                dto_fields.add(arg)
                
            func_lines = lines[func.lineno - 1 : func.end_lineno]
            
            def_idx = 0
            for i, line in enumerate(func_lines):
                if line.strip().startswith("def "):
                    def_idx = i
                    break
            body_lines = func_lines[def_idx + 1:]
            
            if body_lines:
                body_text = textwrap.dedent("".join(body_lines))
                indented_body = textwrap.indent(body_text, "        ")
            else:
                indented_body = "        pass\n"

            unpack_code = ""
            if args:
                unpack_code = "        # Unpack input fields from context\n"
                for arg in args:
                    unpack_code += f"        # {arg} = context.{arg}\n"
                unpack_code += "\n"
                
            step_code = (
                "from typing import Any\n"
                "from wpipe import step, to_obj\n"
                "from dto.context import RefactoredContext\n\n"
                "@step(\n"
                f"    name=\"{step_name}\",\n"
                "    version=\"v1.0\",\n"
                "    timeout=30,\n"
                f"    description=\"Auto-refactored step from function {func_name}\",\n"
                ")\n"
                f"class {step_name}:\n"
                "    def __call__(self, context: Any) -> Any:\n"
                f"{unpack_code}"
                f"{indented_body}\n"
                "        return context\n"
            )
            steps.append((step_name, clean_name, step_code))

    dto_content = (
        "from pydantic import BaseModel\n"
        "from typing import Optional, Dict, Any\n\n"
        "class RefactoredContext(BaseModel):\n"
        "    \"\"\"Shared context containing properties auto-extracted during refactoring.\"\"\"\n"
    )
    if dto_fields:
        for field in sorted(dto_fields):
            dto_content += f"    {field}: Optional[Any] = None\n"
    else:
        dto_content += "    data: Dict[str, Any] = {}\n"
        
    with open(os.path.join(app_dir, "dto", "context.py"), "w", encoding="utf-8") as f:
        f.write(dto_content)
        
    with open(os.path.join(app_dir, "dto", "__init__.py"), "w", encoding="utf-8") as f:
        f.write("from .context import RefactoredContext\n")

    for step_name, clean_name, step_code in steps:
        with open(os.path.join(app_dir, "states", f"{clean_name}.py"), "w", encoding="utf-8") as f:
            f.write(step_code)
            
    states_init = ""
    for step_name, clean_name, _ in steps:
        states_init += f"from .{clean_name} import {step_name}\n"
    with open(os.path.join(app_dir, "states", "__init__.py"), "w", encoding="utf-8") as f:
        f.write(states_init)

    imports_str = ""
    instantiations_str = ""
    for step_name, clean_name, _ in steps:
        imports_str += f"from states.{clean_name} import {step_name}\n"
        instantiations_str += f"        {step_name}(),\n"
        
    pipelines_content = (
        f"{imports_str}"
        "from wpipe import Pipeline\n\n"
        "def build_pipeline() -> Pipeline:\n"
        "    pipeline = Pipeline(\n"
        "        pipeline_name=\"refactored_pipeline\",\n"
        "        pipeline_version=\"1.0.0\",\n"
        "        tracking_db=\"output/tracking.db\",\n"
        "        collect_system_metrics=True\n"
        "    )\n"
        "    pipeline.set_steps([\n"
        f"{instantiations_str}"
        "    ])\n"
        "    return pipeline\n"
    )
    with open(os.path.join(app_dir, "pipelines.py"), "w", encoding="utf-8") as f:
        f.write(pipelines_content)

    main_content = (
        "import sys\n"
        "from wpipe.exception.api_error import ProcessError\n"
        "from pipelines import build_pipeline\n\n"
        "def main():\n"
        "    pipeline = build_pipeline()\n"
        "    try:\n"
        "        # Pass initial parameters matching RefactoredContext\n"
        "        result = pipeline.run({})\n"
        "        print(\"Pipeline execution completed successfully.\")\n"
        "        return result\n"
        "    except ProcessError as e:\n"
        "        print(f\"Pipeline execution failed: {e}\", file=sys.stderr)\n"
        "        sys.exit(1)\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n"
    )
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_content)

    with open(os.path.join(app_dir, "config", "__init__.py"), "w") as f: f.write("")
    with open(os.path.join(app_dir, "model", ".gitkeep"), "w") as f: f.write("")
    with open(os.path.join(app_dir, "services", "__init__.py"), "w") as f: f.write("")
    with open(os.path.join(app_dir, "utils", "__init__.py"), "w") as f: f.write("")
    
    with open(os.path.join(target_dir, "requirements.txt"), "w") as f:
        f.write("wpipe>=1.0.0\npydantic>=2.0.0\n")
    with open(os.path.join(target_dir, "wpipe.config.json"), "w") as f:
        f.write('{\n  "enableBackupFile": true,\n  "maxSearchFiles": 500\n}\n')

    with open(os.path.join(app_dir, "test", "README.md"), "w") as f:
        f.write(
            "# Unit Tests Directory\n\n"
            "This directory is designated for unit and integration testing of the microservice components using `pytest`.\n\n"
            "### How to Execute:\n"
            "Execute tests from the project root directory inside your development environment or container using:\n"
            "```bash\n"
            "pytest app/test/\n"
            "```\n"
        )

    document_wpipe_project(target_dir, write_to_readme=True)

    return f"Success: Monolith refactored successfully into target directory '{target_dir}'."


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
        preexec_fn=os.setpgrp,
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
                "env": {},
            }
        }
    }

    config_json = json.dumps(config, indent=2)

    helper_text = (
        "\n=========================================\n"
        "🔌 QUICK INSTALL COMMANDS FOR AI AGENTS\n"
        "=========================================\n\n"
        "For Gemini CLI:\n"
        f"  gemini mcp add wpipe-mcp {python_path} -m wpipe_mcp.server run\n\n"
        "For Claude Desktop / Cursor:\n"
        "  Copy the JSON above (or from the saved file) into your agent's config file.\n"
        "=========================================\n"
    )

    if not write_file:
        print(config_json)
        print(helper_text)
        return

    # Create .agents directory in the current working directory
    target_dir = os.getcwd()
    agents_dir = os.path.join(target_dir, ".agents")
    os.makedirs(agents_dir, exist_ok=True)

    config_path = os.path.join(agents_dir, "wpipe-mcp.json")
    with open(config_path, "w") as f:
        f.write(config_json)

    print(f"✅ Configuration saved to: {config_path}")
    print(helper_text)


# --- Main Entry Point ---


def main():
    parser = argparse.ArgumentParser(
        description="wpipe-mcp: WPipe Architect MCP Server"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["run", "run-sse", "start", "stop", "config", "help"],
        help="Command to execute (default: run)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print configuration to stdout instead of saving to .agents/",
    )

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
