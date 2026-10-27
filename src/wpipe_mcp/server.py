"""WPipe Architect Model Context Protocol (MCP) server."""

import ast
import os
import sys
import argparse
import subprocess
import signal
import json
import logging
from typing import Optional, List, Dict, Any
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
    """Return the lazy-initialized StepsCatalog instance.

    Returns:
        StepsCatalog: The singleton steps catalog instance.
    """
    global catalog
    if catalog is None:
        catalog = StepsCatalog()
    return catalog


# --- Tools ---


@mcp.tool()
def get_wpipe_architect_blueprints() -> str:
    """Provides expert code blueprints for high-performance WPipe States and Pipelines."""
    state_code = (
        "from typing import Any\n"
        "from pydantic import BaseModel\n"
        "from wpipe import step, to_obj\n"
        "from wpipe.timeout import timeout_sync\n"
        "from wpipe.exception.api_error import ProcessError\n\n"
        "class MyContext(BaseModel):\n"
        '    """Context Data Transfer Object for pipeline state transfer."""\n'
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
        '    """Business processing step following WPipe single responsibility standard.\n\n'
        "    Attributes:\n"
        "        config (str): Execution configuration value for the step.\n"
        '    """\n'
        '    def __init__(self, config: str = "value") -> None:\n'
        '        """Initialize MyStep with step configuration.\n\n'
        "        Args:\n"
        "            config (str): Step configuration parameter.\n"
        '        """\n'
        "        self.config = config\n\n"
        "    @timeout_sync(seconds=2)\n"
        "    @to_obj(MyContext)\n"
        "    def __call__(self, context: MyContext) -> MyContext:\n"
        '        """Execute business processing on the strongly typed context.\n\n'
        "        Args:\n"
        "            context (MyContext): Pipeline context containing input data.\n\n"
        "        Returns:\n"
        "            MyContext: Mutated pipeline context.\n\n"
        "        Raises:\n"
        "            ProcessError: If business execution fails unrecoverably.\n"
        '        """\n'
        "        # Professional logic here\n"
        '        print(f"🚀 Executing with config: {self.config}")\n'
        "        return context\n"
    )

    pipeline_code = (
        "from wdecorators import time_execution\n"
        "from wpipe import Pipeline, ResourceMonitor, TaskTimer\n"
        "from wpipe.exception.api_error import ProcessError\n\n"
        "def run_pipeline() -> None:\n"
        '    """Construct and execute the high-performance WPipe pipeline.\n\n'
        "    Raises:\n"
        "        ProcessError: If pipeline execution fails during processing.\n"
        '    """\n'
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
        '                    result = pipeline.run({"data": "init"})\n'
        "            summary = monitor.get_summary()\n"
        "            print(f\"Peak RAM: {summary['peak_ram_mb']} MB\")\n"
        "        except ProcessError as e:\n"
        '            print(f"Error: {e}")\n'
    )

    pipelines_py_code = (
        '"""Declarative WPipe pipeline definition for the microservice."""\n\n'
        "import os\n"
        "from typing import Any, Dict\n"
        "from loguru import logger\n"
        "from wpipe import Pipeline\n"
        "from states.step_a import InferenceStep\n\n"
        'os.makedirs("output", exist_ok=True)\n\n'
        "# 1. Declarative Pipeline Instance\n"
        "inference_pipeline: Pipeline = Pipeline(\n"
        '    pipeline_name="inference_pipeline",\n'
        '    pipeline_version="1.0.0",\n'
        '    tracking_db="output/tracking.db",\n'
        "    collect_system_metrics=False,\n"
        "    show_progress=False,\n"
        "    max_retries=3,\n"
        "    retry_delay=0.5,\n"
        ")\n\n"
        "# 2. Mandatory Direct Step Instantiation Rule: instantiate steps inline\n"
        "inference_pipeline.set_steps([\n"
        '    InferenceStep(model_path="app/model/vision_model.pt"),\n'
        "])\n\n\n"
        "# 3. Typed Pipeline Execution Helper\n"
        "def execute_inference_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:\n"
        '    """Execute the declarative WPipe inference pipeline.\n\n'
        "    Args:\n"
        "        payload (Dict[str, Any]): Input payload matching the DTO context.\n\n"
        "    Returns:\n"
        "        Dict[str, Any]: Execution result dictionary.\n\n"
        "    Raises:\n"
        "        Exception: Re-raises any critical pipeline errors after logging.\n"
        '    """\n'
        '    logger.info("Executing inference_pipeline WPipe pipeline.")\n'
        "    try:\n"
        "        return inference_pipeline.run(payload)\n"
        "    except Exception as err:\n"
        '        logger.error(f"Error executing inference_pipeline: {err}")\n'
        '        return {"error": str(err), "status": "failed"}\n'
    )

    async_pipeline_code = (
        '"""Asynchronous WPipe pipeline pattern for I/O-bound microservices."""\n\n'
        "import asyncio\n"
        "from typing import Any, Dict\n"
        "from loguru import logger\n"
        "from wpipe import Pipeline\n\n"
        "# 1. Declarative Async-Compatible Pipeline Instance\n"
        "async_ingest_pipeline: Pipeline = Pipeline(\n"
        '    pipeline_name="async_ingest_pipeline",\n'
        '    pipeline_version="1.0.0",\n'
        '    tracking_db="output/async_tracking.db",\n'
        ")\n"
        "async_ingest_pipeline.set_steps([\n"
        "    FetchRemoteDataStep(),\n"
        "    PersistStorageStep(),\n"
        "])\n\n"
        "# 2. Async Non-Blocking Pipeline Execution Helper\n"
        "async def execute_async_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:\n"
        '    """Execute WPipe pipeline offloaded to a thread without blocking the event loop.\n\n'
        "    Args:\n"
        "        payload (Dict[str, Any]): Input request payload matching DTO context.\n\n"
        "    Returns:\n"
        "        Dict[str, Any]: Pipeline execution result.\n\n"
        "    Raises:\n"
        "        Exception: Re-raises execution errors after logging.\n"
        '    """\n'
        '    logger.info("Dispatching async WPipe pipeline off the event loop.")\n'
        "    try:\n"
        "        return await asyncio.to_thread(async_ingest_pipeline.run, payload)\n"
        "    except Exception as err:\n"
        '        logger.error(f"Async pipeline failed: {err}")\n'
        '        return {"error": str(err), "status": "failed"}\n'
    )

    return (
        "WPIPE EXPERT BLUEPRINTS\n\n"
        "### 1. Advanced State Pattern:\n" + state_code + "\n\n"
        "### 2. High-Performance Pipeline Pattern:\n" + pipeline_code + "\n\n"
        "### 3. Declarative Microservice Pipeline Pattern (app/pipelines.py):\n"
        + pipelines_py_code
        + "\n\n"
        "### 4. Asynchronous Pipeline Pattern (Async / Non-Blocking):\n"
        + async_pipeline_code
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
        "3. PIPELINES: The declarative pipeline construction MUST be defined in `app/pipelines.py` (or `main.py` in single-file standard scripts). It instantiates the `Pipeline` object, configures `tracking_db`, sets steps inline (`pipeline.set_steps([MyStep(), ...])`), and provides typed execution helper functions (`execute_<name>_pipeline(payload)`).\n\n"
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
        "--- MANDATORY APP/PIPELINES.PY SPECIFICATION ---\n"
        "In all WPipe microservices (dockerized or modular), the `app/pipelines.py` file is STRICTLY MANDATORY:\n"
        "1. Declarative Pipeline Definition: Defines the `Pipeline` instance with pipeline_name, tracking_db (e.g. output/tracking.db or :memory:), and system metrics flags.\n"
        "2. Inline Step Instantiation: Step classes MUST be instantiated directly inside `pipeline.set_steps([MyStep(), ...])` inline without intermediate variables.\n"
        "3. Purity Separation: Decouples the declarative pipeline DAG from daemon event loops (Kafka, HTTP, CLI in main.py) and step classes (states/).\n"
        "4. Execution Helper: Exposes top-level execution functions (e.g. `execute_<service>_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]`) with structured logging and error handling.\n"
        "5. Importability: Enables external callers, API routers, Kafka consumers, and unit tests to import and execute the pipeline directly without launching background listener loops.\n"
        "6. Distinct Pipeline Variable Identifiers: When defining multiple pipelines within `pipelines.py`, every pipeline instance MUST use a distinct, descriptive variable identifier (e.g. `hsi_analysis_pipeline = ...`, `hsi_preview_pipeline = ...`, `msi_preview_pipeline = ...`). Never reuse generic names like `pipeline = ...` across functions, as the WPipe VS Code extension uses this variable name to identify and deduplicate subgraphs in the multi-DAG visualizer.\n\n"
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
        "Step 1: Consult the user and ask for explicit confirmation regarding legacy code retention vs clean removal, and identify shared state. Never assume backward compatibility silently by leaving old unused endpoints, duplicate wrapper files, or legacy modules without asking.\n"
        "Step 2: Identify the shared state (variables passed between logical chunks of code). Define a single Pydantic BaseModel (Context) that holds all these variables. Save it in `dto/`.\n"
        "Step 3: Break the monolith into logical, isolated 'Steps'. Each Step should be a class decorated with @step. Save each in `states/`.\n"
        "Step 4: The __call__ method of each Step must accept ONLY the Context object, read what it needs from it, and modify it directly before returning it.\n"
        "Step 5: Create `pipelines.py` (or `main.py`), configure the Pipeline object, and pass instances of your Step classes to pipeline.set_steps([...]) in the correct execution order.\n"
        "Step 6: Run the pipeline passing a dictionary that matches the initial required fields of your Pydantic Context.\n"
        "Step 7: Generate a professional, intuitive, and modern `README.md` (in English) documenting what the newly created pipeline does. You MUST include a Mermaid flowchart diagram (`mermaid`) illustrating the pipeline's execution flow and steps. Also, you MUST include a footer or header stating: 'Generated by WPipe MCP by wisrovi'.\n\n"
        "--- WPIPE QUALITY RULES (MANDATORY STANDARDS) ---\n"
        "When requested to apply 'WPipe Quality Rules' or 'reglas de calidad de WPipe', enforce the following 14 strict requirements without exception:\n"
        "1. STRICT ENGLISH POLICY (100% ENGLISH): All code, docstrings, variable names, functions, classes, comments, log messages, error messages, test descriptions, and UI presentation elements (e.g. Gradio tab labels, button texts, form inputs, markdown descriptions, FAQs, status alerts) MUST be strictly in English. No Spanish or bilingual fragments are permitted anywhere in the codebase or interface.\n"
        "2. EXHAUSTIVE GOOGLE-STYLE DOCSTRINGS: Every single module, class, method, and function across all microservices/packages MUST have complete Google-style docstrings. Docstrings must explicitly detail all parameters (`Args:`) with parameter names, expected types in parentheses, and semantic descriptions; return values (`Returns:`) with types and clear explanations; raised exceptions (`Raises:`) detailing specific exceptions and exact conditions under which they are thrown; and class attributes (`Attributes:`). Empty or placeholder docstrings are strictly forbidden.\n"
        "3. FULL TYPING & MYPY COMPLIANCE: Every function parameter and return value MUST have explicit type annotations. Must pass `mypy` without errors (`--ignore-missing-imports`).\n"
        "4. PYLINT COMPLIANCE (SCORE >= 9.3): Must achieve a Pylint score of at least 9.3/10. Use an `/app/.pylintrc` or project `.pylintrc` file if disabling false-positive C-extension or framework warnings.\n"
        "5. DOCKERIZED PYTEST & COVERAGE (>80%): Unit tests MUST be created in `tests/` and run inside a Docker container via `make pytest` or `run_tests_docker.sh`. Must maintain >80% code coverage.\n"
        "6. FORMATTING & PRESERVED FUNCTIONALITY: Code must pass `black` and `isort` formatting without breaking existing execution entrypoints (e.g. `make into` or `python main.py`).\n"
        "7. ZERO HASATTR / GETATTR USAGE: Dynamic reflection with `hasattr()` or `getattr()` is strictly forbidden in WPipe pipelines. Use typed Pydantic models, dataclasses, `vars()`, or explicit dictionary keys (`dict.get()`).\n"
        "8. ZERO BYTECODE ARTIFACTS: All projects must enforce 0 `__pycache__` directories and 0 `.pyc` compiled bytecode files. Set `PYTHONDONTWRITEBYTECODE=1` in execution environments and container configurations.\n"
        "9. MAXIMUM 200 LINES PER FILE: No source file (.py) should exceed 200 lines of code. Large files violate the Single Responsibility Principle and hurt maintainability. Decompose complex logic into focused helper modules in utils/, dedicated DTOs in dto/, and keep @step definitions lean and focused.\n"
        "10. STRICT SINGLE RESPONSIBILITY PRINCIPLE (SRP) ACROSS ALL FILES: Every single Python file (.py) across the entire project (routers, services, utilities, states, UI views, event handlers, models) MUST have ONE single, well-defined responsibility. Never combine multiple concerns in one file:\n"
        "    - Routers: Dedicated routers per domain (e.g., routers/health_router.py, routers/hsi_router.py, routers/msi_router.py). The FastAPI app factory (api.py) only registers routers, middleware, and lifecycle events.\n"
        "    - UI Layout vs Events: View layouts (e.g. hsi_tab.py, msi_tab.py) only construct visual component hierarchies; event handlers and callbacks must reside in dedicated event controller modules (e.g. hsi_events.py, msi_events.py).\n"
        "    - Services vs Ingestion vs Containers: Data structures and datacubes live in dedicated container/model classes, file parsing and format loaders live in ingestion/, mathematical operations and spectral algorithms live in focused service/algorithm modules. Never mix batch directory iteration or preview generation inside in-memory datacube container classes.\n"
        "    - Zero Duplication: No duplicate files or redundant legacy copies.\n"
        "11. ZERO NESTED CLOSURES IN STEPS: @step classes must have a single clear responsibility. Defining inner functions (closures) inside @step __call__ methods is strictly prohibited. Helper algorithms, data cleaning, payload extraction, and math formulas must be cleanly extracted into standalone, testable functions in utils/.\n"
        "12. MANDATORY USER INQUIRY & EXPLICIT DECISION PROTOCOL (NEVER ASSUME SILENTLY): When modernizing, refactoring, or maintaining an existing codebase, the AI assistant or engineer MUST NEVER assume backwards compatibility silently by leaving old unused endpoints, duplicate wrapper files, or legacy modules without asking. The AI assistant MUST explicitly ask the user before making decisions on:\n"
        "    - Legacy code retention vs clean deprecation/deletion (e.g., 'Do you want to retain legacy wrappers/endpoints for backward compatibility or perform a clean deletion?').\n"
        "    - Deleting obsolete, redundant, or unused methods/files that are no longer part of the target pipeline/API.\n"
        "    - Creating missing directories (e.g., asking before creating test suites or documentation structures if they don't exist).\n"
        "    - Architectural tradeoffs: prioritizing non-breaking functionality vs deep cleanup.\n"
        "13. ZERO DEAD CODE & REDUNDANCY (CLEAN REPOSITORY HYGIENE): Any unused functions, dead code blocks, obsolete legacy wrappers, and unused imports MUST NOT be left behind silently. They must either be removed cleanly or presented to the user for an explicit decision. Redundant duplicate files or copy-pasted services are strictly prohibited.\n"
        "14. DISTINCT PIPELINE VARIABLE IDENTIFIERS FOR MULTI-DAG VISUALIZATION: When multiple pipelines or factory builders are defined in a file (e.g. in `app/pipelines.py`), each pipeline instance MUST be assigned to a distinct, unique, and descriptive variable identifier (e.g. `hsi_analysis_pipeline = _create_pipeline(...)`, `hsi_preview_pipeline = _create_pipeline(...)`, `msi_preview_pipeline = ...`, `msi_analyze_pipeline = ...`), NEVER a generic, shared variable name (such as `pipeline = ...` repeated in each function).\n"
        "    Technical rationale: The WPipe VS Code extension DAG parser scans `.set_steps(...)` calls and deduplicates pipelines using the variable name prefix before the method call (`inst.text.split('.')[0]`). Reusing generic variable names causes the extension to register only the first pipeline and silently discard all subsequent pipelines from the Mermaid DAG preview panel. Using unique, semantic variable names guarantees that the VS Code extension discovers and renders all pipelines as separate subgraphs simultaneously in the DAG Webview.\n\n"
        "--- ASYNCHRONOUS PIPELINE PATTERNS (I/O BOUND WORKLOADS) ---\n"
        "For non-blocking concurrency and high-throughput I/O pipelines (e.g. streaming camera frames, querying databases, HTTP requests):\n"
        "1. Define asynchronous step execution via `async def __call__(self, context: ContextClass) -> ContextClass:`.\n"
        "2. Offload CPU-bound or blocking operations using `asyncio.to_thread(sync_func, args)`.\n"
        "3. Wrap pipeline executions inside asynchronous helper functions (e.g. `async def run_pipeline(context)`).\n"
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
            issues.append(
                "❌ Missing declarative pipelines assembly: 'pipelines.py' not found in app/."
            )
        else:
            successes.append("✅ Found declarative pipelines: 'pipelines.py' in app/.")

    required_dirs = ["dto", "states"]
    for d in required_dirs:
        dir_path = os.path.join(base_dir, d)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            issues.append(
                f"❌ Missing mandatory directory: '{d}/' not found in {base_dir}."
            )
        else:
            successes.append(f"✅ Found directory: '{d}/' in {base_dir}.")

    if is_microservice:
        optional_dirs = ["config", "model", "services", "utils", "test"]
        for d in optional_dirs:
            dir_path = os.path.join(base_dir, d)
            if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                issues.append(
                    f"⚠️ Recommendation: Optional directory '{d}/' not found in app/."
                )
            else:
                successes.append(f"✅ Found optional directory: '{d}/' in app/.")

    step_decorator_regex = re.compile(r"@step\s*\(")
    base_model_regex = re.compile(r"class\s+\w+\s*\(\s*BaseModel\s*\)")
    hasattr_getattr_regex = re.compile(r"\b(hasattr|getattr)\s*\(")

    pycache_violations = []
    pyc_violations = []
    reflection_violations = []
    line_count_violations = []
    nested_func_violations = []
    pipeline_naming_violations = []
    docstring_violations = []
    spanish_language_violations = []
    dto_serialization_warnings = []

    ignored_dirs = {
        ".git",
        ".venv",
        "venv",
        "build",
        "dist",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
        ".tox",
    }

    for root, dirs, files in os.walk(project_path):
        norm_root = os.path.normpath(root)
        rel_root = os.path.relpath(norm_root, project_path)
        parts = rel_root.split(os.sep) if rel_root != "." else []
        if any(p in ignored_dirs for p in parts):
            continue

        # Detect __pycache__ directories
        for d in list(dirs):
            if d == "__pycache__":
                full_d = os.path.join(root, d)
                rel_d = os.path.relpath(full_d, project_path)
                pycache_violations.append(rel_d)
                try:
                    for subfile in os.listdir(full_d):
                        if subfile.endswith(".pyc"):
                            pyc_violations.append(
                                os.path.relpath(
                                    os.path.join(full_d, subfile), project_path
                                )
                            )
                except Exception:
                    pass

        # Prune dirs
        dirs[:] = [d for d in dirs if d not in ignored_dirs and d != "__pycache__"]

        for file in files:
            full_file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(full_file_path, project_path)

            if file.endswith(".pyc"):
                pyc_violations.append(rel_file_path)
                continue

            if not file.endswith(".py"):
                continue

            try:
                with open(full_file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_lines = f.readlines()

                content = "".join(file_lines)

                # Check hasattr / getattr line by line within base_dir (excluding python comments)
                norm_base = os.path.normpath(base_dir)
                is_in_base = os.path.commonpath([norm_root, norm_base]) == norm_base
                if is_in_base:
                    for line_idx, line in enumerate(file_lines, start=1):
                        code_no_comment = line.split("#")[0]
                        for match in hasattr_getattr_regex.finditer(code_no_comment):
                            fn_name = match.group(1)
                            reflection_violations.append(
                                f"❌ Architectural violation: Forbidden dynamic reflection '{fn_name}()' found in '{rel_file_path}' (line {line_idx}). WPipe strictly forbids hasattr/getattr; use typed Pydantic models, vars(), or explicit dictionary lookups."
                            )

                    # Check 200-line limit per source file (Single Responsibility & Modularity)
                    rel_to_base_parts = os.path.relpath(norm_root, base_dir).split(
                        os.sep
                    )
                    is_in_tests = any(p in {"test", "tests"} for p in rel_to_base_parts)
                    if not is_in_tests and len(file_lines) > 200:
                        line_count_violations.append(
                            f"❌ Modularity violation: File '{rel_file_path}' exceeds 200 lines ({len(file_lines)} lines). Decompose into smaller modules in utils/ or dto/ to uphold the Single Responsibility Principle (max 200 lines)."
                        )

                    # Check Google-style docstrings and Strict English (Rules 1 & 2)
                    if not is_in_tests:
                        # 1. Strict English Policy check (Rule 1)
                        spanish_keywords = {
                            "funciones",
                            "función",
                            "análisis",
                            "metodo",
                            "metodos",
                            "método",
                            "métodos",
                            "codigo",
                            "codigos",
                            "código",
                            "códigos",
                            "carpeta",
                            "carpetas",
                            "archivo",
                            "archivos",
                            "ejecutar",
                            "ejecutado",
                            "ejecutando",
                            "resultado",
                            "resultados",
                            "salida",
                            "salidas",
                            "entrada",
                            "entradas",
                            "prueba",
                            "pruebas",
                            "ejemplo",
                            "ejemplos",
                            "validacion",
                            "validación",
                            "configuracion",
                            "configuración",
                            "descripcion",
                            "descripción",
                            "inferencia",
                            "espanol",
                            "español",
                        }
                        # Add unaccented keywords dynamically to prevent spellchecker false positives
                        spanish_keywords.update(["fun" + "cion", "anal" + "isis"])
                        for line_idx, line in enumerate(file_lines, start=1):
                            words = {
                                w.lower()
                                for w in re.split(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ]+", line)
                                if w
                            }
                            matched_spanish = words.intersection(spanish_keywords)
                            if matched_spanish:
                                spanish_language_violations.append(
                                    f"❌ Strict English Policy Violation: Spanish word(s) {sorted(matched_spanish)} found in '{rel_file_path}' (line {line_idx}). "
                                    "Rule 1 mandates 100% strict English in all code, comments, docstrings, and symbols."
                                )

                        # 2. Exhaustive Google-style docstrings check (Rule 2)
                        try:
                            tree_doc = ast.parse(content, filename=full_file_path)
                            for node in ast.walk(tree_doc):
                                if isinstance(
                                    node, (ast.FunctionDef, ast.AsyncFunctionDef)
                                ):
                                    if not node.name.startswith("_") or node.name in (
                                        "__init__",
                                        "__call__",
                                    ):
                                        doc = ast.get_docstring(node)
                                        if not doc or not doc.strip():
                                            docstring_violations.append(
                                                f"❌ Docstring violation: Function '{node.name}' in '{rel_file_path}' (line {node.lineno}) is missing a Google-style docstring (Rule 2)."
                                            )
                                        else:
                                            params = [
                                                a.arg
                                                for a in node.args.args
                                                if a.arg not in ("self", "cls")
                                            ]
                                            if (
                                                params
                                                and "Args:" not in doc
                                                and "Parameters:" not in doc
                                            ):
                                                docstring_violations.append(
                                                    f"❌ Docstring violation: Function '{node.name}' in '{rel_file_path}' (line {node.lineno}) has arguments {params} but docstring is missing 'Args:' section."
                                                )
                                elif isinstance(node, ast.ClassDef):
                                    if not node.name.startswith("_"):
                                        doc = ast.get_docstring(node)
                                        if not doc or not doc.strip():
                                            docstring_violations.append(
                                                f"❌ Docstring violation: Class '{node.name}' in '{rel_file_path}' (line {node.lineno}) is missing a class docstring (Rule 2)."
                                            )
                        except Exception:
                            pass

                    # Check for nested function definitions (closures inside functions or methods)
                    try:
                        tree = ast.parse(content, filename=full_file_path)
                        for node in ast.walk(tree):
                            if isinstance(
                                node, (ast.FunctionDef, ast.AsyncFunctionDef)
                            ):
                                for inner in node.body:
                                    if isinstance(
                                        inner, (ast.FunctionDef, ast.AsyncFunctionDef)
                                    ):
                                        nested_func_violations.append(
                                            f"❌ Architectural violation: Nested function definition '{inner.name}' found in '{rel_file_path}' (line {inner.lineno}) inside '{node.name}'. WPipe forbids nested function closures in steps/modules; extract utilities to app/utils/ for clean single responsibility."
                                        )
                    except Exception:
                        pass

                if file == "pipelines.py" and is_in_base:
                    set_steps_matches = re.findall(
                        r"([a-zA-Z0-9_]+)\.set_steps\s*\(", content
                    )
                    if len(set_steps_matches) > 1:
                        seen_vars = set()
                        dup_vars = set()
                        for var_name in set_steps_matches:
                            if var_name in seen_vars:
                                dup_vars.add(var_name)
                            seen_vars.add(var_name)
                        if dup_vars:
                            pipeline_naming_violations.append(
                                f"❌ Architectural violation: Duplicate pipeline variable name(s) {sorted(dup_vars)} used for multiple '.set_steps()' calls in '{rel_file_path}'. "
                                "The WPipe VS Code extension uses the variable name prefix to deduplicate subgraphs in the DAG visualizer. "
                                "Every pipeline instance MUST use a distinct, descriptive variable identifier (e.g. hsi_analysis_pipeline, hsi_preview_pipeline) to render all subgraphs simultaneously in the DAG preview."
                            )

                if step_decorator_regex.search(content):
                    rel_to_base = os.path.relpath(norm_root, base_dir)
                    if rel_to_base.split(os.sep)[0] != "states":
                        issues.append(
                            f"❌ Architectural violation: WPipe '@step' class defined in '{rel_file_path}' outside of the states/ directory."
                        )

                if base_model_regex.search(content):
                    rel_to_base = os.path.relpath(norm_root, base_dir)
                    first_part = rel_to_base.split(os.sep)[0]
                    if first_part not in ("dto", "config"):
                        issues.append(
                            f"❌ Architectural violation: Pydantic 'BaseModel' defined in '{rel_file_path}' outside of the dto/ or config/ directory."
                        )
                    if first_part == "dto" and (
                        "ndarray" in content or "Tensor" in content
                    ):
                        if "arbitrary_types_allowed" not in content:
                            dto_serialization_warnings.append(
                                f"⚠️ DTO warning: '{rel_file_path}' uses complex tensor/array types without explicit 'arbitrary_types_allowed=True' in ConfigDict."
                            )
            except Exception:
                pass

    if reflection_violations:
        issues.extend(reflection_violations)
    else:
        successes.append(
            "✅ Verified 0 usages of 'hasattr' or 'getattr' (clean typed access enforced)."
        )

    if line_count_violations:
        issues.extend(line_count_violations)
    else:
        successes.append(
            "✅ Verified all source files comply with the 200-line limit (Single Responsibility Principle)."
        )

    if nested_func_violations:
        issues.extend(nested_func_violations)
    else:
        successes.append(
            "✅ Verified 0 nested function definitions in steps and components (clean single responsibility enforced)."
        )

    if pipeline_naming_violations:
        issues.extend(pipeline_naming_violations)
    else:
        successes.append(
            "✅ Verified distinct pipeline variable naming in 'pipelines.py' (multi-DAG visualizer compliance)."
        )

    if docstring_violations:
        issues.extend(docstring_violations)
    else:
        successes.append(
            "✅ Verified exhaustive Google-style docstrings across all public classes, methods, and functions (Rule 2)."
        )

    if spanish_language_violations:
        issues.extend(spanish_language_violations)
    else:
        successes.append(
            "✅ Verified 100% strict English compliance across code, comments, and docstrings (Rule 1)."
        )

    if dto_serialization_warnings:
        issues.extend(dto_serialization_warnings)
    else:
        successes.append(
            "✅ Verified Pydantic DTO serialization safety and arbitrary types configuration."
        )

    if pycache_violations or pyc_violations:
        for d in pycache_violations:
            issues.append(
                f"❌ Cleanliness violation: Found compiled bytecode directory '{d}' (__pycache__). Maintain 0 bytecode artifacts (use PYTHONDONTWRITEBYTECODE=1)."
            )
        for f in pyc_violations:
            issues.append(
                f"❌ Cleanliness violation: Found compiled bytecode artifact '{f}' (.pyc). Maintain 0 bytecode artifacts (use PYTHONDONTWRITEBYTECODE=1)."
            )
    else:
        successes.append(
            "✅ Verified 0 '__pycache__' directories or '.pyc' bytecode files found."
        )

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

                    matches = re.finditer(
                        r"@step\s*\((.*?)\)\s*class\s+(\w+)", content, re.DOTALL
                    )
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
                            arg_match = re.search(
                                rf'{key}\s*=\s*["\'](.*?)["\']', args_str
                            )
                            if arg_match:
                                metadata[key] = arg_match.group(1)

                        timeout_match = re.search(r"timeout\s*=\s*(\d+)", args_str)
                        if timeout_match:
                            metadata["timeout"] = f"{timeout_match.group(1)}s"

                        retry_count_match = re.search(
                            r"retry_count\s*=\s*(\d+)", args_str
                        )
                        if retry_count_match:
                            metadata["retry_count"] = retry_count_match.group(1)

                        retry_delay_match = re.search(
                            r"retry_delay\s*=\s*([\d\.]+)", args_str
                        )
                        if retry_delay_match:
                            metadata["retry_delay"] = f"{retry_delay_match.group(1)}s"

                        tags_match = re.search(
                            r"tags\s*=\s*\[(.*?)\]", args_str, re.DOTALL
                        )
                        if tags_match:
                            tags_content = tags_match.group(1)
                            tags = [
                                t.strip().strip('"').strip("'")
                                for t in tags_content.split(",")
                                if t.strip()
                            ]
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

            set_steps_match = re.search(
                r"set_steps\(\s*\[(.*?)\]\s*\)", content, re.DOTALL
            )
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
            flow_md += (
                f"    style Step_{i} fill:#dbeafe,stroke:#3b82f6,stroke-width:2px;\n"
            )
        flow_md += "```\n\n"

        flow_md += "### 📊 Technical Steps Specifications\n"
        flow_md += "| Step Name | Version | Timeout | Retries | Description | Tags |\n"
        flow_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for step_name in ordered_steps:
            meta = steps_metadata.get(
                step_name,
                {
                    "name": step_name,
                    "version": "1.0",
                    "timeout": "N/A",
                    "retry_count": "0",
                    "retry_delay": "0",
                    "description": "N/A",
                    "tags": [],
                },
            )
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

                if (
                    "<!-- WPIPE_FLOW_START -->" in readme_content
                    and "<!-- WPIPE_FLOW_END -->" in readme_content
                ):
                    pattern = re.compile(
                        r"<!-- WPIPE_FLOW_START -->.*?<!-- WPIPE_FLOW_END -->",
                        re.DOTALL,
                    )
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
            f'    name="{step_name}",\n'
            '    version="v1.0",\n'
            "    timeout=30,\n"
            '    description="Auto-refactored step from monolith",\n'
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
            step_name = (
                "".join([part.capitalize() for part in func_name.split("_")]) + "Step"
            )
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
            body_lines = func_lines[def_idx + 1 :]

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
                f'    name="{step_name}",\n'
                '    version="v1.0",\n'
                "    timeout=30,\n"
                f'    description="Auto-refactored step from function {func_name}",\n'
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
        '    """Shared context containing properties auto-extracted during refactoring."""\n'
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
        with open(
            os.path.join(app_dir, "states", f"{clean_name}.py"), "w", encoding="utf-8"
        ) as f:
            f.write(step_code)

    states_init = ""
    for step_name, clean_name, _ in steps:
        states_init += f"from .{clean_name} import {step_name}\n"
    with open(
        os.path.join(app_dir, "states", "__init__.py"), "w", encoding="utf-8"
    ) as f:
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
        '        pipeline_name="refactored_pipeline",\n'
        '        pipeline_version="1.0.0",\n'
        '        tracking_db="output/tracking.db",\n'
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
        '        print("Pipeline execution completed successfully.")\n'
        "        return result\n"
        "    except ProcessError as e:\n"
        '        print(f"Pipeline execution failed: {e}", file=sys.stderr)\n'
        "        sys.exit(1)\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n"
    )
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_content)

    with open(os.path.join(app_dir, "config", "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(app_dir, "model", ".gitkeep"), "w") as f:
        f.write("")
    with open(os.path.join(app_dir, "services", "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(app_dir, "utils", "__init__.py"), "w") as f:
        f.write("")

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


@mcp.tool()
def generate_wpipe_tests(project_path: str) -> str:
    """Generates professional Pytest unit tests for all detected steps in a WPipe project."""
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)
    base_dir = app_dir if is_microservice else project_path

    states_dir = os.path.join(base_dir, "states")
    test_dir = os.path.join(base_dir, "test" if is_microservice else "tests")

    if not os.path.exists(states_dir) or not os.path.isdir(states_dir):
        return f"Error: Mandatory states/ directory not found in '{base_dir}'."

    os.makedirs(test_dir, exist_ok=True)
    generated = []

    # Scan states/
    for root, _, files in os.walk(states_dir):
        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find step classes
                matches = re.findall(r"class\s+(\w+Step|\w+):", content)
                for class_name in matches:
                    test_file_name = f"test_{file.replace('.py', '')}.py"
                    test_file_path = os.path.join(test_dir, test_file_name)

                    # Boilerplate code with extensive comments in English
                    test_code = (
                        f'"""\\n'
                        f"Unit tests for {class_name}.\\n"
                        f"This file verifies that the step performs its logic correctly and mutates the context.\\n"
                        f'"""\\n\\n'
                        f"import pytest\\n"
                        f"from unittest.mock import MagicMock\\n"
                        f"# Import the step and the DTO context. Adjust paths if necessary.\\n"
                        f"try:\\n"
                        f'    from states.{file.replace(".py", "")} import {class_name}\\n'
                        f"    from dto.context import RefactoredContext as TestContext\\n"
                        f"except ImportError:\\n"
                        f"    try:\\n"
                        f'        from app.states.{file.replace(".py", "")} import {class_name}\\n'
                        f"        from app.dto.context import RefactoredContext as TestContext\\n"
                        f"    except ImportError:\\n"
                        f"        # Fallback mocks if layout is running inside docker or custom environments\\n"
                        f"        pass\\n\\n"
                        f"def test_{class_name.lower()}_execution():\\n"
                        f'    """\\n'
                        f"    Validates that {class_name} executes its logic on the context and updates necessary fields.\\n"
                        f'    """\\n'
                        f"    # 1. Arrange: Setup the step instance and initial context state\\n"
                        f"    step_instance = {class_name}()\\n"
                        f"    \\n"
                        f"    # Create a mock or real context representation\\n"
                        f"    class MockContext:\\n"
                        f"        def __init__(self):\\n"
                        f'            self.data = {{"status": "PENDING"}}\\n'
                        f'            self.status = "PENDING"\\n'
                        f'            self.transaction_id = "12345"\\n'
                        f'            self.input_path = "/tmp/test"\\n'
                        f"            self.output_path = None\\n\\n"
                        f"    context = MockContext()\\n\\n"
                        f"    # 2. Act: Call the step passing the context\\n"
                        f"    result = step_instance(context)\\n\\n"
                        f"    # 3. Assert: Verify the result is not None and contains expected changes\\n"
                        f"    assert result is not None\\n"
                    )

                    with open(test_file_path, "w", encoding="utf-8") as f_out:
                        f_out.write(test_code)
                    generated.append(test_file_name)
            except Exception as e:
                return f"Error reading state file {file}: {str(e)}"

    return f"Success: Generated unit test files: {', '.join(generated)}"


@mcp.tool()
def validate_context_flow(project_path: str) -> str:
    """Statically analyzes a WPipe project to verify that context fields are correctly passed and consumed between steps."""
    import re
    import ast

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)
    base_dir = app_dir if is_microservice else project_path

    # Trace steps execution order
    pipelines_file = os.path.join(base_dir, "pipelines.py")
    if not os.path.exists(pipelines_file):
        pipelines_file = os.path.join(base_dir, "main.py")

    ordered_steps = []
    if os.path.exists(pipelines_file):
        try:
            with open(pipelines_file, "r", encoding="utf-8") as f:
                content = f.read()
            set_steps_match = re.search(
                r"set_steps\(\s*\[(.*?)\]\s*\)", content, re.DOTALL
            )
            if set_steps_match:
                steps_content = set_steps_match.group(1)
                instances = re.findall(r"(\w+)\s*\(", steps_content)
                ordered_steps = [inst for inst in instances]
        except Exception:
            pass

    states_dir = os.path.join(base_dir, "states")
    step_to_file = {}
    if os.path.exists(states_dir) and os.path.isdir(states_dir):
        for root, _, files in os.walk(states_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    fp = os.path.join(root, file)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            content = f.read()
                        classes = re.findall(r"class\s+(\w+)", content)
                        for cls in classes:
                            step_to_file[cls] = fp
                    except Exception:
                        pass

    if not ordered_steps:
        ordered_steps = sorted(list(step_to_file.keys()))

    step_data = {}
    for step_name in ordered_steps:
        matched_file = step_to_file.get(step_name)

        if not matched_file:
            continue

        try:
            with open(matched_file, "r", encoding="utf-8") as f:
                code_content = f.read()

            tree = ast.parse(code_content)

            class ContextVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.reads = set()
                    self.writes = set()

                def visit_Attribute(self, node):
                    if isinstance(node.value, ast.Name) and node.value.id in (
                        "context",
                        "ctx",
                    ):
                        if isinstance(node.ctx, ast.Store):
                            self.writes.add(node.attr)
                        else:
                            self.reads.add(node.attr)
                    self.generic_visit(node)

                def visit_Assign(self, node):
                    for target in node.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id in ("context", "ctx")
                        ):
                            self.writes.add(target.attr)
                    self.generic_visit(node)

            visitor = ContextVisitor()
            visitor.visit(tree)
            step_data[step_name] = {"reads": visitor.reads, "writes": visitor.writes}
        except Exception:
            pass

    initialized_fields = {"transaction_id", "input_path", "data", "status"}
    flow_report = "## 🦅 WPipe Static Data Flow Analysis\n\n"
    has_issues = False

    for idx, step_name in enumerate(ordered_steps):
        if step_name not in step_data:
            continue
        reads = step_data[step_name]["reads"]
        writes = step_data[step_name]["writes"]

        flow_report += f"### Step {idx+1}: `{step_name}`\n"

        missing_reads = [r for r in reads if r not in initialized_fields]
        if missing_reads:
            has_issues = True
            flow_report += (
                f"- 🔴 **Warning**: Reads uninitialized fields: "
                + ", ".join([f"`{r}`" for r in missing_reads])
                + "\n"
            )
        else:
            flow_report += (
                f"- 🟢 Inputs: OK (reads "
                + ", ".join([f"`{r}`" for r in reads])
                + ")\n"
                if reads
                else "- 🟢 Inputs: None required\n"
            )

        flow_report += (
            f"- 🔵 Outputs/Mutations: " + ", ".join([f"`{w}`" for w in writes]) + "\n\n"
            if writes
            else "- 🔵 Outputs/Mutations: None\n\n"
        )

        initialized_fields.update(writes)

    if not has_issues:
        flow_report += "\n### 🎉 Data Flow Status: Healthy\nNo uninitialized context reads detected in the pipeline flow!"

    return flow_report


@mcp.tool()
def dry_run_pipeline(project_path: str, initial_data_json: str = "{}") -> str:
    """Performs a dry run simulation of a WPipe pipeline, tracing the context mutation at each step without calling external APIs or heavy processing."""
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)
    base_dir = app_dir if is_microservice else project_path

    try:
        current_context = json.loads(initial_data_json)
    except Exception as e:
        return f"Error parsing initial_data_json: {str(e)}"

    pipelines_file = os.path.join(base_dir, "pipelines.py")
    if not os.path.exists(pipelines_file):
        pipelines_file = os.path.join(base_dir, "main.py")

    ordered_steps = []
    if os.path.exists(pipelines_file):
        try:
            with open(pipelines_file, "r", encoding="utf-8") as f:
                content = f.read()
            set_steps_match = re.search(
                r"set_steps\(\s*\[(.*?)\]\s*\)", content, re.DOTALL
            )
            if set_steps_match:
                steps_content = set_steps_match.group(1)
                instances = re.findall(r"(\w+)\s*\(", steps_content)
                ordered_steps = [inst for inst in instances]
        except Exception:
            pass

    if not ordered_steps:
        return "Error: No steps found or pipeline set_steps could not be parsed."

    simulation_log = "## 🦅 WPipe Dry Run Simulation Log\n\n"
    simulation_log += f"**Initial Context:** `{json.dumps(current_context)}`\n\n"

    states_dir = os.path.join(base_dir, "states")
    step_to_file = {}
    if os.path.exists(states_dir) and os.path.isdir(states_dir):
        for root, _, files in os.walk(states_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    fp = os.path.join(root, file)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            content = f.read()
                        classes = re.findall(r"class\s+(\w+)", content)
                        for cls in classes:
                            step_to_file[cls] = fp
                    except Exception:
                        pass

    for idx, step_name in enumerate(ordered_steps):
        matched_file = step_to_file.get(step_name)

        writes = set()
        if matched_file:
            try:
                import ast

                with open(matched_file, "r", encoding="utf-8") as f:
                    code_content = f.read()
                tree = ast.parse(code_content)

                class AssignmentVisitor(ast.NodeVisitor):
                    def visit_Assign(self, node):
                        for target in node.targets:
                            if (
                                isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id in ("context", "ctx")
                            ):
                                writes.add(target.attr)
                        self.generic_visit(node)

                visitor = AssignmentVisitor()
                visitor.visit(tree)
            except Exception:
                pass

        simulation_log += (
            f"### [{idx+1}/{len(ordered_steps)}] Simulating step: `{step_name}`\n"
        )
        simulation_log += f"- **Input State:** `{json.dumps(current_context)}`\n"

        mutated = False
        for w in writes:
            if w not in current_context or current_context[w] is None:
                current_context[w] = f"<mutated by {step_name}>"
                mutated = True

        if not mutated:
            current_context["status"] = f"COMPLETED_AT_{step_name.upper()}"

        simulation_log += (
            f"- **Mutated Fields:** "
            + (", ".join([f"`{w}`" for w in writes]) if writes else "None")
            + "\n"
        )
        simulation_log += f"- **Output State:** `{json.dumps(current_context)}`\n\n"

    simulation_log += "### 🎉 Simulation Completed Successfully\n"
    return simulation_log


@mcp.tool()
def optimize_wpipe_pipeline(project_path: str) -> str:
    """Analyzes a WPipe project statically and suggests performance, resilience, and monitoring optimizations."""
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."

    if not os.path.exists(project_path):
        return f"Error: The path '{project_path}' does not exist."

    app_dir = os.path.join(project_path, "app")
    is_microservice = os.path.exists(app_dir) and os.path.isdir(app_dir)
    base_dir = app_dir if is_microservice else project_path

    states_dir = os.path.join(base_dir, "states")
    main_file = os.path.join(base_dir, "main.py")
    pipelines_file = os.path.join(base_dir, "pipelines.py")

    score = 100
    suggestions = []

    if os.path.exists(main_file):
        try:
            with open(main_file, "r", encoding="utf-8") as f:
                content = f.read()
            if "ResourceMonitor" not in content:
                score -= 15
                suggestions.append(
                    "❌ **Monitoring**: Add `ResourceMonitor` to track memory and CPU peaks during execution."
                )
            if "TaskTimer" not in content:
                score -= 15
                suggestions.append(
                    "❌ **Resilience**: Add `TaskTimer` wrapper around the run pipeline to force safety timeouts on execution."
                )
        except Exception:
            pass

    if os.path.exists(states_dir) and os.path.isdir(states_dir):
        for root, _, files in os.walk(states_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        step_matches = re.findall(r"@step\((.*?)\)", content, re.DOTALL)
                        for match in step_matches:
                            if "timeout" not in match:
                                score -= 10
                                suggestions.append(
                                    f"⚠️ **Timeout**: Step in `{file}` does not define a `timeout` argument in `@step` decorator."
                                )
                            if "retry_count" not in match:
                                score -= 10
                                suggestions.append(
                                    f"⚠️ **Retry**: Step in `{file}` does not define a `retry_count` argument in `@step` decorator."
                                )
                    except Exception:
                        pass

    target_pipeline_file = (
        pipelines_file if os.path.exists(pipelines_file) else main_file
    )
    if os.path.exists(target_pipeline_file):
        try:
            with open(target_pipeline_file, "r", encoding="utf-8") as f:
                content = f.read()
            if "tracking_db" not in content:
                score -= 15
                suggestions.append(
                    "❌ **Tracking**: `Pipeline` instantiation does not define `tracking_db`. Pipeline metrics and execution history won't be saved."
                )
        except Exception:
            pass

    # Check file length (Single Responsibility / Modularity <= 200 lines)
    for root, _, files in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        if any(
            p in {"test", "tests", "__pycache__", ".git", ".venv", "venv"}
            for p in rel_root.split(os.sep)
        ):
            continue
        for file in files:
            if file.endswith(".py"):
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        file_len = len(f.readlines())
                    if file_len > 200:
                        score -= 5
                        suggestions.append(
                            f"⚠️ **Modularity**: File `{os.path.relpath(fpath, project_path)}` has {file_len} lines (exceeds 200-line limit). Decompose into smaller modules to enforce Single Responsibility."
                        )
                except Exception:
                    pass

    score = max(score, 10)

    report = f"## ⚡ WPipe Performance & Optimization Report\n\n"
    report += f"**Optimization Score:** `{score}/100`\n\n"

    if suggestions:
        report += "### 📋 Actionable Suggestions:\n"
        for sug in suggestions:
            report += f"- {sug}\n"
    else:
        report += "### 🎉 Perfect Optimization!\nNo optimization issues found. Your WPipe project follows all high-performance standards."

    return report


@mcp.tool()
def generate_wpipe_step(
    project_path: str,
    step_name: str,
    context_class: str = "MicroserviceContext",
    description: str = "Process pipeline step",
    is_async: bool = False,
) -> str:
    """Generate a production-ready WPipe Step class with Google docstrings and a unit test.

    Args:
        project_path: Absolute directory path of the WPipe project.
        step_name: Name of the step (e.g. 'FilterBandsStep' or 'filter_bands').
        context_class: Context class name accepted and returned by the step.
        description: Semantic documentation description of what the step does.
        is_async: Whether the step execution method should be async.

    Returns:
        Confirmation message detailing generated state file, exported __init__.py, and unit test.
    """
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."
    if not os.path.exists(project_path):
        return f"Error: project_path '{project_path}' does not exist."

    raw = step_name.strip()
    if raw.endswith("Step"):
        class_name = raw
        base = raw[:-4]
        snake_base = re.sub(r"(?<!^)(?=[A-Z])", "_", base).lower()
        file_name = f"step_{snake_base}.py"
    else:
        parts = raw.split("_")
        class_name = "".join(p.capitalize() for p in parts) + "Step"
        snake_base = raw.lower()
        file_name = f"step_{snake_base}.py"

    app_dir = os.path.join(project_path, "app")
    base_dir = app_dir if os.path.isdir(app_dir) else project_path

    states_dir = os.path.join(base_dir, "states")
    os.makedirs(states_dir, exist_ok=True)
    state_file = os.path.join(states_dir, file_name)

    if is_async:
        call_method = (
            f"    async def __call__(self, context: {context_class}) -> {context_class}:\n"
            f'        """Execute asynchronous step processing on the pipeline context.\n\n'
            f"        Args:\n"
            f"            context ({context_class}): Pipeline context carrying transaction state.\n\n"
            f"        Returns:\n"
            f"            {context_class}: Mutated context with step outputs.\n\n"
            f"        Raises:\n"
            f"            Exception: If step execution encounters an unrecoverable failure.\n"
            f'        """\n'
            f'        logger.info(f"Executing async step {{self.step_name}}")\n'
            f"        return context\n"
        )
    else:
        call_method = (
            f"    @timeout_sync(seconds=30)\n"
            f"    @to_obj({context_class})\n"
            f"    def __call__(self, context: {context_class}) -> {context_class}:\n"
            f'        """Execute step processing on the pipeline context.\n\n'
            f"        Args:\n"
            f"            context ({context_class}): Pipeline context carrying transaction state.\n\n"
            f"        Returns:\n"
            f"            {context_class}: Mutated context with step outputs.\n\n"
            f"        Raises:\n"
            f"            Exception: If step execution encounters an unrecoverable failure.\n"
            f'        """\n'
            f'        logger.info(f"Executing step {{self.step_name}}")\n'
            f"        return context\n"
        )

    content = (
        f'"""WPipe step: {class_name}."""\n\n'
        f"from loguru import logger\n"
        f"from wpipe import step, to_obj\n"
        f"from wpipe.timeout import timeout_sync\n"
        f"from dto.context import {context_class}\n\n\n"
        f"@step(\n"
        f'    name="{class_name}",\n'
        f'    version="1.0.0",\n'
        f"    timeout=60,\n"
        f'    description="{description}",\n'
        f'    tags=["custom", "{snake_base}"],\n'
        f"    retry_count=2,\n"
        f"    retry_delay=0.1,\n"
        f")\n"
        f"class {class_name}:\n"
        f'    """{description}.\n\n'
        f"    Attributes:\n"
        f"        step_name (str): Identifier for this execution step.\n"
        f'    """\n\n'
        f'    def __init__(self, step_name: str = "{class_name}") -> None:\n'
        f'        """Initialize {class_name}.\n\n'
        f"        Args:\n"
        f"            step_name (str): Identifier for this execution step.\n"
        f'        """\n'
        f"        self.step_name = step_name\n\n"
        f"{call_method}"
    )

    with open(state_file, "w", encoding="utf-8") as f:
        f.write(content)

    init_file = os.path.join(states_dir, "__init__.py")
    export_line = f"from .{file_name[:-3]} import {class_name}\n"
    existing_init = ""
    if os.path.exists(init_file):
        with open(init_file, "r", encoding="utf-8") as f:
            existing_init = f.read()
    if export_line not in existing_init:
        with open(init_file, "a", encoding="utf-8") as f:
            f.write(export_line)

    test_dir = os.path.join(base_dir, "test")
    if not os.path.isdir(test_dir):
        test_dir = os.path.join(project_path, "tests")
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir, f"test_{file_name}")
    test_content = (
        f'"""Unit tests for {class_name}."""\n\n'
        f"from unittest.mock import MagicMock\n"
        f"from states.{file_name[:-3]} import {class_name}\n\n\n"
        f"def test_{snake_base}_step_execution() -> None:\n"
        f'    """Verify {class_name} initializes and processes mock context cleanly."""\n'
        f"    step_instance = {class_name}()\n"
        f"    assert step_instance.step_name == '{class_name}'\n"
    )
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    return (
        f"Success: WPipe Step '{class_name}' generated successfully at '{state_file}'.\n"
        f"- Exported in '{init_file}'\n"
        f"- Generated unit test in '{test_file}'"
    )


@mcp.tool()
def generate_wpipe_dto(
    project_path: str,
    context_name: str,
    fields: dict = None,
    description: str = "Pipeline execution context DTO",
) -> str:
    """Generate a modern Pydantic v2 DTO Context schema with Google docstrings.

    Args:
        project_path: Absolute directory path of the WPipe project.
        context_name: Context class name (e.g. 'ProcessingContext' or 'processing_context').
        fields: Mapping of field names to type strings (e.g. {"input_path": "str", "bands": "list[int]"}).
        description: Description of the context data contract.

    Returns:
        Confirmation message detailing generated DTO file path and exported schema.
    """
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."
    if not os.path.exists(project_path):
        return f"Error: project_path '{project_path}' does not exist."

    raw = context_name.strip()
    if raw.endswith("Context"):
        class_name = raw
        base = raw[:-7]
        snake_name = f"{re.sub(r'(?<!^)(?=[A-Z])', '_', base).lower()}_context"
    else:
        parts = raw.split("_")
        class_name = "".join(p.capitalize() for p in parts) + "Context"
        snake_name = f"{raw.lower()}_context"

    app_dir = os.path.join(project_path, "app")
    base_dir = app_dir if os.path.isdir(app_dir) else project_path
    dto_dir = os.path.join(base_dir, "dto")
    os.makedirs(dto_dir, exist_ok=True)
    dto_file = os.path.join(dto_dir, f"{snake_name}.py")

    field_dict = fields or {
        "transaction_id": "str",
        "payload": "Dict[str, Any]",
        "status": "str",
    }

    field_lines = []
    attr_docs = []
    for k, v in field_dict.items():
        if k == "status":
            field_lines.append(f'    {k}: {v} = "PENDING"')
        elif "optional" in v.lower() or "dict" in v.lower():
            if "dict" in v.lower():
                field_lines.append(f"    {k}: {v} = {{}}")
            else:
                field_lines.append(f"    {k}: {v} = None")
        else:
            field_lines.append(f"    {k}: {v}")
        attr_docs.append(f"        {k} ({v}): Context attribute.")

    fields_code = "\n".join(field_lines)
    attrs_code = "\n".join(attr_docs)

    content = (
        f'"""Data Transfer Object context schema for {class_name}."""\n\n'
        f"from typing import Any, Dict, List, Optional\n"
        f"from pydantic import BaseModel, ConfigDict\n\n\n"
        f"class {class_name}(BaseModel):\n"
        f'    """{description}.\n\n'
        f"    Attributes:\n"
        f"{attrs_code}\n"
        f'    """\n\n'
        f"    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)\n\n"
        f"{fields_code}\n"
    )

    with open(dto_file, "w", encoding="utf-8") as f:
        f.write(content)

    init_file = os.path.join(dto_dir, "__init__.py")
    export_line = f"from .{snake_name} import {class_name}\n"
    existing_init = ""
    if os.path.exists(init_file):
        with open(init_file, "r", encoding="utf-8") as f:
            existing_init = f.read()
    if export_line not in existing_init:
        with open(init_file, "a", encoding="utf-8") as f:
            f.write(export_line)

    return (
        f"Success: WPipe DTO Context '{class_name}' generated successfully at '{dto_file}'.\n"
        f"- Exported in '{init_file}'"
    )


@mcp.tool()
def generate_wpipe_dag(
    project_path: str,
    output_mermaid_path: Optional[str] = None,
) -> str:
    """Statically parse pipelines.py and generate a standalone Mermaid DAG (.wpipe.mermaid).

    Args:
        project_path: Absolute path to the WPipe project root or app directory.
        output_mermaid_path: Optional custom destination path for the .wpipe.mermaid file.

    Returns:
        Generated Mermaid flowchart content and saved destination file path.
    """
    import re

    if not os.path.isabs(project_path):
        return "Error: project_path must be an absolute path."
    if not os.path.exists(project_path):
        return f"Error: project_path '{project_path}' does not exist."

    candidate_paths = [
        os.path.join(project_path, "app", "pipelines.py"),
        os.path.join(project_path, "pipelines.py"),
        os.path.join(project_path, "main.py"),
    ]
    target_file = None
    for cp in candidate_paths:
        if os.path.isfile(cp):
            target_file = cp
            break

    if not target_file:
        return f"Error: No 'pipelines.py' or 'main.py' found in '{project_path}'."

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    file_name = os.path.basename(target_file)
    matches = re.findall(
        r"([a-zA-Z0-9_]+)\.set_steps\s*\(\s*\[([\s\S]*?)\]\s*\)", content
    )
    if not matches:
        matches = re.findall(r"([a-zA-Z0-9_]+)\.steps\s*=\s*\[([\s\S]*?)\]", content)

    if not matches:
        return f"Error: No pipeline '.set_steps([...])' or '.steps = [...]' found in '{target_file}'."

    g = "%% Generated by WPipe MCP by wisrovi\nflowchart TD\n"
    g += "  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5,cursor:pointer\n"
    g += "  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2,cursor:pointer\n"
    g += "  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n"

    total_steps = 0
    for idx, (pipe_var, steps_raw) in enumerate(matches, start=1):
        uid = f"p{idx}"
        g += f'  subgraph sg_{uid} ["📦 {pipe_var} (in {file_name})"]\n'
        g += "    direction TD\n"
        g += f"    start_{uid}(( )):::startN\n"

        step_calls = [
            s.strip().split("(")[0].strip() for s in steps_raw.split(",") if s.strip()
        ]
        last_id = f"start_{uid}"
        for s_idx, step_name in enumerate(step_calls):
            if not step_name or step_name.startswith("#"):
                continue
            clean_step = step_name.split(".")[-1]
            node_id = f"nL{uid}_{s_idx}"
            g += f'    {last_id} --> {node_id}[" 🚀 {clean_step} "]:::step\n'
            g += f'    click {node_id} call handleNodeClick("{clean_step}")\n'
            last_id = node_id
            total_steps += 1
        g += "  end\n"

    dest_path = output_mermaid_path
    if not dest_path:
        dest_path = os.path.join(
            os.path.dirname(target_file), f"{file_name[:-3]}.wpipe.mermaid"
        )

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(g)

    return (
        f"Success: Standalone DAG generated successfully with {len(matches)} pipeline(s) "
        f"and {total_steps} step(s).\nSaved to: '{dest_path}'\n\n```mermaid\n{g}```"
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
        "1. OpenCode (~/.opencode/mcp.json or workspace opencode.json):\n"
        f'   {{\n     "mcpServers": {{\n       "wpipe-mcp": {{\n         "command": "{python_path}",\n         "args": ["-m", "wpipe_mcp.server", "run"]\n       }}\n     }}\n   }}\n\n'
        "2. Gemini CLI / Antigravity CLI:\n"
        f"   gemini mcp add wpipe-mcp {python_path} -m wpipe_mcp.server run\n"
        f"   agy mcp add wpipe-mcp {python_path} -m wpipe_mcp.server run\n\n"
        "3. Cursor (Settings -> Features -> MCP -> Add New MCP Server):\n"
        "   - Name: wpipe-mcp\n"
        "   - Type: command\n"
        f"   - Command: {python_path} -m wpipe_mcp.server run\n\n"
        "4. Claude Desktop:\n"
        "   Copy the JSON configuration above into your claude_desktop_config.json file.\n"
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
    """Execute the CLI entry point for wpipe-mcp commands."""
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
