"""Advanced scaffolding templates for professional WPipe development."""


class TemplateGenerator:
    """Provides professional boilerplate for WPipe projects following wisrovi standards."""

    @staticmethod
    def get_supported_types() -> list:
        """Return the list of supported scaffolding architecture types.

        Returns:
            list: Supported pipeline type identifiers.
        """
        return ["standard", "ai_vision_mlops", "microservice"]

    @staticmethod
    def get_folders(pipeline_type: str) -> list:
        """Return the folder hierarchy required for the given pipeline architecture.

        Args:
            pipeline_type (str): Selected pipeline architecture type.

        Returns:
            list: List of directory paths to create.
        """
        if pipeline_type == "ai_vision_mlops":
            return [
                "config",
                "dto",
                "states",
                "inference",
                "training",
                "datasets",
                "tests",
                ".wpipe",
            ]
        elif pipeline_type == "microservice":
            return [
                "app",
                "app/config",
                "app/dto",
                "app/model",
                "app/services",
                "app/states",
                "app/test",
                "app/utils",
                ".wpipe",
            ]
        return ["config", "dto", "states", "tests", ".wpipe"]

    @staticmethod
    def get_files_blueprint(
        pipeline_type: str,
        project_name: str = "wpipe_project",
        include_tests: bool = True,
    ) -> dict:
        """Returns filenames and their professional template content."""
        if pipeline_type == "microservice":
            return TemplateGenerator._get_microservice_blueprint(
                project_name, include_tests
            )

        return TemplateGenerator._get_standard_blueprint(pipeline_type, project_name)

    @staticmethod
    def _get_microservice_blueprint(project_name: str, include_tests: bool) -> dict:
        config_yaml = (
            f"# Configuration for {project_name}\n"
            'microservice_name: "{name}"\n'
            'environment: "development"\n'
            "debug: true\n"
        ).format(name=project_name)

        settings_py = (
            "import os\n"
            "from pydantic import BaseModel\n\n"
            "class AppSettings(BaseModel):\n"
            '    """Typed settings loaded from environment or configurations."""\n'
            '    environment: str = os.getenv("APP_ENV", "development")\n'
            '    debug: bool = os.getenv("APP_DEBUG", "True").lower() == "true"\n'
        )

        dto_context = (
            "from typing import Any, Dict, Optional\n"
            "from pydantic import BaseModel, ConfigDict\n\n"
            "class MicroserviceContext(BaseModel):\n"
            '    """Data Transfer Object defining the shared context for the WPipe pipeline.\n\n'
            "    Attributes:\n"
            "        transaction_id (str): Unique transaction identifier.\n"
            "        input_path (str): File system path to the input data.\n"
            "        output_path (Optional[str]): Processed output artifact path.\n"
            "        metrics (Dict[str, Any]): Telemetry and evaluation metrics dictionary.\n"
            "        status (str): Processing lifecycle state (e.g. PENDING, PROCESSED).\n"
            '    """\n'
            "    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)\n\n"
            "    transaction_id: str\n"
            "    input_path: str\n"
            "    output_path: Optional[str] = None\n"
            "    metrics: Dict[str, Any] = {}\n"
            '    status: str = "PENDING"\n'
        )

        state_step = (
            "from typing import Any\n"
            "from wpipe import step, to_obj\n"
            "from wpipe.timeout import timeout_sync\n"
            "from dto.context import MicroserviceContext\n"
            "from services.vision_service import VisionInferenceService\n\n"
            "@step(\n"
            '    name="InferenceStep",\n'
            '    version="v1.0",\n'
            "    timeout=15,\n"
            '    description="State responsible for execution of machine learning inference",\n'
            '    tags=["inference", "ml"],\n'
            "    retry_count=3,\n"
            "    retry_delay=0.1,\n"
            ")\n"
            "class InferenceStep:\n"
            '    """WPipe State wrapper that calls the underlying decoupled vision service.\n\n'
            "    Attributes:\n"
            "        service (VisionInferenceService): Decoupled inference engine.\n"
            '    """\n'
            '    def __init__(self, model_path: str = "app/model/vision_model.pt") -> None:\n'
            '        """Initialize InferenceStep with model path.\n\n'
            "        Args:\n"
            "            model_path (str): File system path to model weights.\n"
            '        """\n'
            "        self.service = VisionInferenceService(model_path=model_path)\n\n"
            "    @timeout_sync(seconds=5)\n"
            "    @to_obj(MicroserviceContext)\n"
            "    def __call__(self, context: MicroserviceContext) -> MicroserviceContext:\n"
            '        """Execute inference step on the pipeline context.\n\n'
            "        Args:\n"
            "            context (MicroserviceContext): Pipeline context carrying transaction state.\n\n"
            "        Returns:\n"
            "            MicroserviceContext: Mutated context containing inference results.\n"
            '        """\n'
            '        print(f"Executing step for transaction: {context.transaction_id}")\n'
            "        # Call decoupled business/inference service\n"
            "        inference_result = self.service.run_inference(context.input_path)\n"
            '        context.output_path = inference_result.get("output_file")\n'
            '        context.metrics["confidence"] = inference_result.get("confidence", 0.0)\n'
            '        context.status = "PROCESSED"\n'
            "        return context\n"
        )

        vision_service = (
            "import os\n"
            "from typing import Any, Dict\n\n"
            "class VisionInferenceService:\n"
            '    """Decoupled service handling core machine learning model inference.\n\n'
            "    Attributes:\n"
            "        model_path (str): Path to the serialized neural network weights.\n"
            '    """\n'
            "    def __init__(self, model_path: str) -> None:\n"
            '        """Initialize the vision inference service.\n\n'
            "        Args:\n"
            "            model_path (str): File system path to the model artifact.\n"
            '        """\n'
            "        self.model_path = model_path\n\n"
            "    def run_inference(self, input_path: str) -> Dict[str, Any]:\n"
            '        """Execute model inference on an input image.\n\n'
            "        Args:\n"
            "            input_path (str): Path to the target image file.\n\n"
            "        Returns:\n"
            "            Dict[str, Any]: Inference result dictionary containing output path and confidence.\n\n"
            "        Raises:\n"
            "            FileNotFoundError: If input image does not exist.\n"
            '        """\n'
            "        # Dummy inference logic for scaffolding\n"
            '        if not os.path.exists(input_path) and input_path != "mock_path":\n'
            '            raise FileNotFoundError(f"Input file not found: {input_path}")\n'
            "        return {\n"
            '            "status": "success",\n'
            '            "output_file": f"{input_path}_processed.png",\n'
            '            "confidence": 0.95,\n'
            "        }\n"
        )

        helpers_py = (
            "import os\n"
            "from typing import Set\n\n"
            "def validate_file_extension(filename: str, allowed: Set[str]) -> bool:\n"
            '    """Pure utility function to validate file extension.\n\n'
            "    Args:\n"
            "        filename (str): Name or path of the target file.\n"
            '        allowed (Set[str]): Allowed extension strings (e.g. {".png", ".jpg"}).\n\n'
            "    Returns:\n"
            "        bool: True if file extension is within allowed set, False otherwise.\n"
            '    """\n'
            "    _, ext = os.path.splitext(filename)\n"
            "    return ext.lower() in allowed\n"
        )

        pipelines_py = (
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
            "    collect_system_metrics=True,\n"
            "    show_progress=True,\n"
            "    max_retries=3,\n"
            "    retry_delay=0.5\n"
            ")\n\n"
            "# 2. Direct inline step assembly\n"
            "inference_pipeline.set_steps([\n"
            '    InferenceStep(model_path="app/model/vision_model.pt")\n'
            "])\n\n\n"
            "def build_inference_pipeline() -> Pipeline:\n"
            '    """Declaratively return the configured WPipe state machine.\n\n'
            "    Returns:\n"
            "        Pipeline: Pre-configured inference state machine.\n"
            '    """\n'
            "    return inference_pipeline\n\n\n"
            "def execute_inference_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:\n"
            '    """Execute the declarative WPipe inference pipeline.\n\n'
            "    Args:\n"
            "        payload (Dict[str, Any]): Input payload matching the DTO context.\n\n"
            "    Returns:\n"
            "        Dict[str, Any]: Execution result dictionary.\n"
            '    """\n'
            '    logger.info("Executing inference_pipeline WPipe pipeline.")\n'
            "    try:\n"
            "        return inference_pipeline.run(payload)\n"
            "    except Exception as err:\n"
            '        logger.error(f"Error executing inference_pipeline: {err}")\n'
            '        return {"error": str(err), "status": "failed"}\n'
        )

        main_py = (
            "import sys\n"
            "from typing import Any, Dict\n"
            "from wpipe.exception.api_error import ProcessError\n"
            "from wpipe import ResourceMonitor, TaskTimer\n"
            "from pipelines import build_inference_pipeline\n\n"
            "def handle_event(event_data: Dict[str, Any]) -> Dict[str, Any]:\n"
            '    """Entry point that receives event trigger, runs pipeline and logs resource usage.\n\n'
            "    Args:\n"
            "        event_data (Dict[str, Any]): Event payload initiating the pipeline run.\n\n"
            "    Returns:\n"
            "        Dict[str, Any]: Pipeline execution result.\n\n"
            "    Raises:\n"
            "        ProcessError: If pipeline execution fails unrecoverably.\n"
            '    """\n'
            "    pipeline = build_inference_pipeline()\n"
            "    \n"
            "    try:\n"
            '        with ResourceMonitor("microservice_monitor") as monitor:\n'
            '            with TaskTimer("microservice_timer", timeout_seconds=900) as timer:\n'
            "                result = pipeline.run(event_data)\n"
            "                \n"
            "        summary = monitor.get_summary()\n"
            '        print(f"Inference successfully finished. Elapsed time: {timer.elapsed_seconds:.2f}s")\n'
            "        print(f\"Memory Peak: {summary.get('peak_ram_mb')} MB\")\n"
            "        return result\n"
            "    except ProcessError as e:\n"
            '        print(f"Pipeline process error: {e}", file=sys.stderr)\n'
            "        raise e\n\n"
            'if __name__ == "__main__":\n'
            '    mock_event = {"transaction_id": "tx_999", "input_path": "mock_path"}\n'
            "    handle_event(mock_event)\n"
        )

        pylintrc = (
            "[MAIN]\n"
            "fail-under=9.3\n"
            "max-line-length=200\n"
            "disable=C0114,C0115,C0116,R0903,W0718,E1101,C0301\n"
        )

        run_tests_docker_sh = (
            "#!/bin/bash\n"
            "set -e\n"
            'echo "=== Running WPipe Microservice Unit Tests via Docker ==="\n'
            "docker run --rm \\\n"
            "  -e PYTHONDONTWRITEBYTECODE=1 \\\n"
            '  -v "$(pwd)":/usr/src/app \\\n'
            "  -w /usr/src/app \\\n"
            "  python:3.11-slim \\\n"
            '  bash -c "pip install -q pytest pytest-cov pydantic wpipe wdecorators loguru && pytest app/test/ --cov=app --cov-report=term-missing --cov-fail-under=80"\n'
            'echo "=== All WPipe tests completed successfully! ==="\n'
        )

        pipelines_wpipe_mermaid = (
            "%% Generated by WPipe Tools\n"
            "flowchart TD\n"
            "  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5,cursor:pointer\n"
            "  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2,cursor:pointer\n"
            "  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n"
            '  subgraph sg_inf ["📦 inference_pipeline (in pipelines.py)"]\n'
            "    direction TD\n"
            "    start_inf(( )):::startN\n"
            '    start_inf --> nLinf0[" 🚀 InferenceStep "]:::step\n'
            '    click nLinf0 call handleNodeClick("InferenceStep")\n'
            "  end\n"
        )

        readme_md = (
            f"# {project_name.upper()}\n\n"
            "Professional internal microservice architecture built with **wpipe**.\n\n"
            "## 🛠️ Key Technologies & Libraries\n"
            "- **WPipe**: State-machine DAG orchestration engine.\n"
            "- **Pydantic v2**: High-performance typed data validation and context schemas.\n"
            "- **Loguru**: Structured, ergonomic logging.\n"
            "- **Pytest & Coverage**: Automated unit test execution (>80% coverage).\n"
            "- **Docker**: Containerized reproducible runtime environments.\n\n"
            "---\n*Generated by WPipe MCP by **wisrovi***\n"
        )

        blueprints = {
            "requirements.txt": "wpipe==2.5.13\nwdecorators==2.2.0\npydantic==2.10.6\nloguru==0.7.3\n",
            ".pylintrc": pylintrc,
            "run_tests_docker.sh": run_tests_docker_sh,
            "README.md": readme_md,
            "app/config/__init__.py": "",
            "app/config/config.yaml": config_yaml,
            "app/config/settings.py": settings_py,
            "app/dto/__init__.py": "from .context import MicroserviceContext\n",
            "app/dto/context.py": dto_context,
            "app/model/.gitkeep": "",
            "app/services/__init__.py": "from .vision_service import VisionInferenceService\n",
            "app/services/vision_service.py": vision_service,
            "app/states/__init__.py": "from .step_a import InferenceStep\n",
            "app/states/step_a.py": state_step,
            "app/utils/__init__.py": "from .helpers import validate_file_extension\n",
            "app/utils/helpers.py": helpers_py,
            "app/pipelines.py": pipelines_py,
            "app/pipelines.wpipe.mermaid": pipelines_wpipe_mermaid,
            "app/main.py": main_py,
            "wpipe.config.json": '{\n  "enableBackupFile": true,\n  "maxSearchFiles": 500\n}\n',
        }

        if include_tests:
            blueprints["app/test/__init__.py"] = ""
            blueprints["app/test/test_dto.py"] = (
                "import pytest\n"
                "from dto.context import MicroserviceContext\n"
                "from pydantic import ValidationError\n\n"
                "def test_context_validation():\n"
                '    """Verify Pydantic schema validation behaves as expected."""\n'
                '    ctx = MicroserviceContext(transaction_id="tx_123", input_path="/tmp/in.png")\n'
                '    assert ctx.transaction_id == "tx_123"\n'
                '    assert ctx.status == "PENDING"\n'
                "    \n"
                "    with pytest.raises(ValidationError):\n"
                "        # Missing transaction_id\n"
                '        MicroserviceContext(input_path="/tmp/in.png")\n'
            )
            blueprints["app/test/test_states.py"] = (
                "from unittest.mock import MagicMock\n"
                "from dto.context import MicroserviceContext\n"
                "from states.step_a import InferenceStep\n\n"
                "def test_inference_step_mutation():\n"
                '    """Verify step execution updates context attributes correctly."""\n'
                '    step = InferenceStep(model_path="mock_model.pt")\n'
                "    # Mock the underlying service to avoid file IO dependencies\n"
                "    step.service.run_inference = MagicMock(return_value={\n"
                '        "output_file": "/tmp/out.png",\n'
                '        "confidence": 0.98\n'
                "    })\n"
                "    \n"
                '    ctx = MicroserviceContext(transaction_id="tx_123", input_path="mock_path")\n'
                "    result = step(ctx)\n"
                "    \n"
                '    assert result.status == "PROCESSED"\n'
                '    assert result.output_path == "/tmp/out.png"\n'
                '    assert result.metrics["confidence"] == 0.98\n'
            )
        else:
            blueprints["app/test/README.md"] = (
                "# Unit Tests Directory\n\n"
                "This directory is designated for unit and integration testing of the microservice components using `pytest`.\n\n"
                "### Recommended Test Coverage:\n"
                "1. **DTO Validation (`test_dto.py`)**: Validate Pydantic schema constraints, path existence checks, and context data types.\n"
                "2. **Service Logic (`test_services.py`)**: Verify decoupled business logic, tabular processors, and machine learning/inference service outputs.\n"
                "3. **WPipe States (`test_states.py`)**: Validate WPipe step lifecycle, transition mutations, timeouts, and state retries.\n\n"
                "### How to Execute:\n"
                "Execute tests from the project root directory inside your development environment or container using:\n"
                "```bash\n"
                "pytest app/test/\n"
                "```\n"
            )

        return blueprints

    @staticmethod
    def _get_standard_blueprint(pipeline_type: str, project_name: str) -> dict:
        dto_template = (
            "from pydantic import BaseModel, ConfigDict\n\n"
            "class ProcessDataContext(BaseModel):\n"
            '    """Typed context defining shared data across pipeline steps.\n\n'
            "    Attributes:\n"
            "        field (str): Example data field processed by steps.\n"
            '    """\n'
            "    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)\n\n"
            "    field: str\n"
        )

        state_template = (
            "from typing import Any\n"
            "from wpipe import step, to_obj\n"
            "from wpipe.timeout import timeout_sync\n"
            "from dto.process_context import ProcessDataContext\n\n"
            "@step(\n"
            '    name="ProcessData",\n'
            '    version="v1.0",\n'
            "    timeout=10,\n"
            '    description="Professional data processing step",\n'
            '    tags=["custom", "processing"],\n'
            "    retry_count=3,\n"
            "    retry_delay=0.01,\n"
            ")\n"
            "class ProcessDataStep:\n"
            '    """Advanced WPipe State: ProcessData.\n\n'
            "    Attributes:\n"
            "        config (str): Execution configuration setting.\n"
            '    """\n'
            '    def __init__(self, config: str = "default_value") -> None:\n'
            '        """Initialize ProcessDataStep with configuration.\n\n'
            "        Args:\n"
            "            config (str): Configuration parameter for the step.\n"
            '        """\n'
            "        self.config = config\n\n"
            "    @timeout_sync(seconds=2)\n"
            "    @to_obj(ProcessDataContext)\n"
            "    def __call__(self, context: ProcessDataContext) -> ProcessDataContext:\n"
            '        """Execute business processing on the pipeline context.\n\n'
            "        Args:\n"
            "            context (ProcessDataContext): Typed context instance.\n\n"
            "        Returns:\n"
            "            ProcessDataContext: Mutated pipeline context.\n"
            '        """\n'
            '        print(f"🚀 Executing ProcessData with config: {self.config}")\n'
            "        return context\n"
        )

        pipeline_template = (
            "import os\n"
            "from typing import Any, Dict\n"
            "from wpipe import Pipeline, ResourceMonitor, TaskTimer\n"
            "from wpipe.exception.api_error import ProcessError\n"
            "from states.process_step import ProcessDataStep\n\n"
            "def run_pipeline() -> Dict[str, Any]:\n"
            '    """Construct and execute the high-performance pipeline.\n\n'
            "    Returns:\n"
            "        Dict[str, Any]: Pipeline execution result dictionary.\n\n"
            "    Raises:\n"
            "        ProcessError: If pipeline execution encounters a processing failure.\n"
            '    """\n'
            '    db_path = "output/tracking.db"  # Metrics, events, and forensics\n'
            '    config_dir = ("configs",)      # Optional YAML/JSON configs\n\n'
            "    pipeline = Pipeline(\n"
            '        pipeline_name="{name}",\n'
            '        pipeline_version="1.0.0",\n'
            "        tracking_db=db_path,\n"
            "        config_dir=config_dir,\n"
            "        verbose=False,\n"
            "        max_retries=3,\n"
            "        retry_delay=0.5,\n"
            "        retry_on_exceptions=(RuntimeError,),\n"
            "        collect_system_metrics=True,\n"
            "        show_progress=True\n"
            "    )\n\n"
            "    pipeline.set_steps([\n"
            '        ProcessDataStep(config="prod")\n'
            "    ])\n\n"
            '    initial_data = {{"field": "init"}}\n\n'
            "    try:\n"
            '        with ResourceMonitor("{name}_monitor") as monitor:\n'
            '            with TaskTimer("{name}_timer", timeout_seconds=900) as timer:\n'
            "                result = pipeline.run(initial_data)\n\n"
            "        summary = monitor.get_summary()\n"
            "        print(f\"Peak RAM: {{summary['peak_ram_mb']}} MB\")\n"
            "        print(f\"Avg CPU: {{summary['avg_cpu_percent']}}%\")\n"
            '        print(f"Total time: {{timer.elapsed_seconds:.2f}}s")\n'
            "        return result\n"
            "    except ProcessError as e:\n"
            '        print(f"Error occurred: {{e}}")\n'
            "        raise e\n\n"
            'if __name__ == "__main__":\n'
            "    run_pipeline()\n"
        ).format(name=project_name)

        readme_md = (
            f"# {project_name.upper()}\n\n"
            "Professional architecture built with **wpipe**.\n\n"
            "## 🛠️ Key Technologies & Libraries\n"
            "- **WPipe**: State-machine DAG orchestration engine.\n"
            "- **Pydantic v2**: High-performance typed data validation and context schemas.\n"
            "- **Pytest**: Unit testing framework.\n\n"
            "---\n*Generated by WPipe MCP by **wisrovi***\n"
        )

        pylintrc = (
            "[MAIN]\n"
            "fail-under=9.3\n"
            "max-line-length=200\n"
            "disable=C0114,C0115,C0116,R0903,W0718,E1101,C0301\n"
        )

        blueprints = {
            "requirements.txt": "wpipe==2.5.13\nwdecorators==2.2.0\npydantic==2.10.6\n",
            ".pylintrc": pylintrc,
            "README.md": readme_md,
            "dto/__init__.py": "from .process_context import ProcessDataContext\n",
            "dto/process_context.py": dto_template,
            "states/__init__.py": "from .process_step import ProcessDataStep\n",
            "states/process_step.py": state_template,
            "main.py": pipeline_template,
            "wpipe.config.json": '{\n  "enableBackupFile": true,\n  "maxSearchFiles": 500\n}\n',
        }

        if pipeline_type == "ai_vision_mlops":
            blueprints[
                "requirements.txt"
            ] += "wyolo==1.0.0\nwtrain==1.0.0\ncelery==5.3.6\n"

        return blueprints
