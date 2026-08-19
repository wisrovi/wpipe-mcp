# Advanced scaffolding templates for professional WPipe development


class TemplateGenerator:
    """Provides professional boilerplate for WPipe projects following wisrovi standards."""

    @staticmethod
    def get_supported_types() -> list:
        return ["standard", "ai_vision_mlops", "microservice"]

    @staticmethod
    def get_folders(pipeline_type: str) -> list:
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
        pipeline_type: str, project_name: str = "wpipe_project", include_tests: bool = True
    ) -> dict:
        """Returns filenames and their professional template content."""
        if pipeline_type == "microservice":
            return TemplateGenerator._get_microservice_blueprint(project_name, include_tests)

        return TemplateGenerator._get_standard_blueprint(pipeline_type, project_name)

    @staticmethod
    def _get_microservice_blueprint(project_name: str, include_tests: bool) -> dict:
        config_yaml = (
            f"# Configuration for {project_name}\n"
            "microservice_name: \"{name}\"\n"
            "environment: \"development\"\n"
            "debug: true\n"
        ).format(name=project_name)

        settings_py = (
            "import os\n"
            "from pydantic import BaseModel\n\n"
            "class AppSettings(BaseModel):\n"
            "    \"\"\"Typed settings loaded from environment or configurations.\"\"\"\n"
            "    environment: str = os.getenv(\"APP_ENV\", \"development\")\n"
            "    debug: bool = os.getenv(\"APP_DEBUG\", \"True\").lower() == \"true\"\n"
        )

        dto_context = (
            "from pydantic import BaseModel\n"
            "from typing import Optional, Dict, Any\n\n"
            "class MicroserviceContext(BaseModel):\n"
            "    \"\"\"Data Transfer Object defining the shared context for the WPipe pipeline.\"\"\"\n"
            "    transaction_id: str\n"
            "    input_path: str\n"
            "    output_path: Optional[str] = None\n"
            "    metrics: Dict[str, Any] = {}\n"
            "    status: str = \"PENDING\"\n"
        )

        state_step = (
            "from typing import Any\n"
            "from wpipe import step, to_obj\n"
            "from wpipe.timeout import timeout_sync\n"
            "from dto.context import MicroserviceContext\n"
            "from services.vision_service import VisionInferenceService\n\n"
            "@step(\n"
            "    name=\"InferenciaStep\",\n"
            "    version=\"v1.0\",\n"
            "    timeout=15,\n"
            "    description=\"State responsible for execution of machine learning inference\",\n"
            "    tags=[\"inference\", \"ml\"],\n"
            "    retry_count=3,\n"
            "    retry_delay=0.1,\n"
            ")\n"
            "class InferenciaStep:\n"
            "    \"\"\"WPipe State wrapper that calls the underlying decoupled vision service.\"\"\"\n"
            "    def __init__(self, model_path: str = \"app/model/vision_model.pt\"):\n"
            "        self.service = VisionInferenceService(model_path=model_path)\n\n"
            "    @timeout_sync(seconds=5)\n"
            "    @to_obj(MicroserviceContext)\n"
            "    def __call__(self, context: Any) -> Any:\n"
            "        print(f\"Executing step for transaction: {context.transaction_id}\")\n"
            "        # Call decoupled business/inference service\n"
            "        inference_result = self.service.run_inference(context.input_path)\n"
            "        context.output_path = inference_result.get(\"output_file\")\n"
            "        context.metrics[\"confidence\"] = inference_result.get(\"confidence\", 0.0)\n"
            "        context.status = \"PROCESSED\"\n"
            "        return context\n"
        )

        vision_service = (
            "import os\n\n"
            "class VisionInferenceService:\n"
            "    \"\"\"Decoupled service handling core machine learning model inference.\"\"\"\n"
            "    def __init__(self, model_path: str):\n"
            "        self.model_path = model_path\n\n"
            "    def run_inference(self, input_path: str) -> dict:\n"
            "        # Dummy inference logic for scaffolding\n"
            "        if not os.path.exists(input_path) and input_path != \"mock_path\":\n"
            "            raise FileNotFoundError(f\"Input file not found: {input_path}\")\n"
            "        return {\n"
            "            \"status\": \"success\",\n"
            "            \"output_file\": f\"{input_path}_processed.png\",\n"
            "            \"confidence\": 0.95,\n"
            "        }\n"
        )

        helpers_py = (
            "import os\n\n"
            "def validate_file_extension(filename: str, allowed: set) -> bool:\n"
            "    \"\"\"Pure utility function to validate file extension.\"\"\"\n"
            "    _, ext = os.path.splitext(filename)\n"
            "    return ext.lower() in allowed\n"
        )

        pipelines_py = (
            "from wpipe import Pipeline\n"
            "from states.step_a import InferenciaStep\n\n"
            "def build_inference_pipeline() -> Pipeline:\n"
            "    \"\"\"Declaratively construct the WPipe state machine.\"\"\"\n"
            "    pipeline = Pipeline(\n"
            "        pipeline_name=\"inference_pipeline\",\n"
            "        pipeline_version=\"1.0.0\",\n"
            "        tracking_db=\"output/tracking.db\",\n"
            "        collect_system_metrics=True,\n"
            "        show_progress=True,\n"
            "        max_retries=3,\n"
            "        retry_delay=0.5\n"
            "    )\n"
            "    # Assemble steps\n"
            "    pipeline.set_steps([\n"
            "        InferenciaStep(model_path=\"app/model/vision_model.pt\")\n"
            "    ])\n"
            "    return pipeline\n"
        )

        main_py = (
            "import sys\n"
            "from wpipe.exception.api_error import ProcessError\n"
            "from wdecorators import time_execution\n"
            "from wpipe import ResourceMonitor, TaskTimer\n"
            "from pipelines import build_inference_pipeline\n\n"
            "def handle_event(event_data: dict):\n"
            "    \"\"\"Entry point that receives event trigger, runs pipeline and logs resource usage.\"\"\"\n"
            "    pipeline = build_inference_pipeline()\n"
            "    \n"
            "    try:\n"
            "        with ResourceMonitor(\"microservice_monitor\") as monitor:\n"
            "            with TaskTimer(\"microservice_timer\", timeout_seconds=900) as timer:\n"
            "                @time_execution\n"
            "                def run():\n"
            "                    return pipeline.run(event_data)\n"
            "                result = run()\n"
            "                \n"
            "        summary = monitor.get_summary()\n"
            "        print(f\"Inference successfully finished. Elapsed time: {timer.elapsed_seconds:.2f}s\")\n"
            "        print(f\"Memory Peak: {summary.get('peak_ram_mb')} MB\")\n"
            "        return result\n"
            "    except ProcessError as e:\n"
            "        print(f\"Pipeline process error: {e}\", file=sys.stderr)\n"
            "        raise e\n\n"
            "if __name__ == \"__main__\":\n"
            "    mock_event = {\"transaction_id\": \"tx_999\", \"input_path\": \"mock_path\"}\n"
            "    handle_event(mock_event)\n"
        )

        blueprints = {
            "requirements.txt": "wpipe>=1.0.0\nwdecorators>=2.0.0\npydantic>=2.0.0\n",
            "README.md": f"# {project_name.upper()}\n\nProfessional internal microservice architecture built with **wpipe**.\n\n---\n*Generated by WPipe MCP by **wisrovi***\n",
            "app/config/__init__.py": "",
            "app/config/config.yaml": config_yaml,
            "app/config/settings.py": settings_py,
            "app/dto/__init__.py": "from .context import MicroserviceContext\n",
            "app/dto/context.py": dto_context,
            "app/model/.gitkeep": "",
            "app/services/__init__.py": "from .vision_service import VisionInferenceService\n",
            "app/services/vision_service.py": vision_service,
            "app/states/__init__.py": "from .step_a import InferenciaStep\n",
            "app/states/step_a.py": state_step,
            "app/utils/__init__.py": "from .helpers import validate_file_extension\n",
            "app/utils/helpers.py": helpers_py,
            "app/pipelines.py": pipelines_py,
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
                "    \"\"\"Verify Pydantic schema validation behaves as expected.\"\"\"\n"
                "    ctx = MicroserviceContext(transaction_id=\"tx_123\", input_path=\"/tmp/in.png\")\n"
                "    assert ctx.transaction_id == \"tx_123\"\n"
                "    assert ctx.status == \"PENDING\"\n"
                "    \n"
                "    with pytest.raises(ValidationError):\n"
                "        # Missing transaction_id\n"
                "        MicroserviceContext(input_path=\"/tmp/in.png\")\n"
            )
            blueprints["app/test/test_states.py"] = (
                "from unittest.mock import MagicMock\n"
                "from dto.context import MicroserviceContext\n"
                "from states.step_a import InferenciaStep\n\n"
                "def test_inferencia_step_mutation():\n"
                "    \"\"\"Verify step execution updates context attributes correctly.\"\"\"\n"
                "    step = InferenciaStep(model_path=\"mock_model.pt\")\n"
                "    # Mock the underlying service to avoid file IO dependencies\n"
                "    step.service.run_inference = MagicMock(return_value={\n"
                "        \"output_file\": \"/tmp/out.png\",\n"
                "        \"confidence\": 0.98\n"
                "    })\n"
                "    \n"
                "    ctx = MicroserviceContext(transaction_id=\"tx_123\", input_path=\"mock_path\")\n"
                "    result = step(ctx)\n"
                "    \n"
                "    assert result.status == \"PROCESSED\"\n"
                "    assert result.output_path == \"/tmp/out.png\"\n"
                "    assert result.metrics[\"confidence\"] == 0.98\n"
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
            "from pydantic import BaseModel\n\n"
            "class ProcessDataContext(BaseModel):\n"
            '    """Typed context for the step."""\n'
            "    field: str\n"
        )

        state_template = (
            "from wpipe import step, to_obj\n"
            "from wpipe.timeout import timeout_sync\n"
            "from typing import Any\n"
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
            '    """\n'
            "    Advanced WPipe State: ProcessData\n"
            "    Generated by wpipe-mcp Architect.\n"
            '    """\n'
            "    \n"
            '    def __init__(self, config: str = "default_value"):\n'
            "        self.config = config\n\n"
            "    @timeout_sync(seconds=2)\n"
            "    @to_obj(ProcessDataContext)\n"
            "    def __call__(self, context: Any) -> Any:\n"
            "        # Professional logic here\n"
            '        print(f"🚀 Executing ProcessData with config: {self.config}")\n'
            "        return context\n"
        )

        pipeline_template = (
            "import os\n"
            "from wdecorators import time_execution\n"
            "from wpipe import Pipeline, ResourceMonitor, TaskTimer\n"
            "from wpipe.exception.api_error import ProcessError\n"
            "from states.process_step import ProcessDataStep\n\n"
            "def run_pipeline():\n"
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
            '            with TaskTimer("{name}_timer", timeout_seconds=900) as timer:\n\n'
            "                @time_execution\n"
            "                def run():\n"
            "                    return pipeline.run(initial_data)\n\n"
            "                result = run()\n"
            "                \n"
            "        summary = monitor.get_summary()\n"
            "        print(f\"Peak RAM: {{summary['peak_ram_mb']}} MB\")\n"
            "        print(f\"Avg CPU: {{summary['avg_cpu_percent']}}%\")\n"
            '        print(f"Total time: {{timer.elapsed_seconds:.2f}}s")\n'
            "        return result\n"
            "    except ProcessError as e:\n"
            '        print(f"Error occurred: {{e}}")\n\n'
            'if __name__ == "__main__":\n'
            "    run_pipeline()\n"
        ).format(name=project_name)

        blueprints = {
            "requirements.txt": "wpipe>=1.0.0\nwdecorators>=2.0.0\npydantic>=2.0.0\n",
            "README.md": f"# {project_name.upper()}\n\nProfessional architecture built with **wpipe**.\n\n---\n*Generated by WPipe MCP by **wisrovi***\n",
            "dto/__init__.py": "from .process_context import ProcessDataContext\n",
            "dto/process_context.py": dto_template,
            "states/__init__.py": "from .process_step import ProcessDataStep\n",
            "states/process_step.py": state_template,
            "main.py": pipeline_template,
            "wpipe.config.json": '{\n  "enableBackupFile": true,\n  "maxSearchFiles": 500\n}\n',
        }

        if pipeline_type == "ai_vision_mlops":
            blueprints["requirements.txt"] += (
                "wyolo>=1.0.0\nwtrain>=1.0.0\ncelery>=5.3.0\n"
            )

        return blueprints
