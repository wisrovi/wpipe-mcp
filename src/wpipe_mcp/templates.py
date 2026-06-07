# Advanced scaffolding templates for professional WPipe development

class TemplateGenerator:
    """Provides professional boilerplate for WPipe projects following wisrovi standards."""

    @staticmethod
    def get_supported_types() -> list:
        return ["standard", "ai_vision_mlops"]

    @staticmethod
    def get_folders(pipeline_type: str) -> list:
        if pipeline_type == "ai_vision_mlops":
            return ["config", "src", "src/inference", "src/training", "src/training/tasks", "src/states", "datasets", "tests", ".wpipe"]
        return ["config", "src", "src/steps", "src/states", "tests", ".wpipe"]

    @staticmethod
    def get_files_blueprint(pipeline_type: str, project_name: str = "wpipe_project") -> dict:
        """Returns filenames and their professional template content."""
        
        # Professional Class-based State Template
        state_template = (
            "from wpipe import step, to_obj, PipelineContext\n"
            "from pydantic import Field\n"
            "from typing import Any\n\n"
            "class MyContext(PipelineContext):\n"
            "    \"\"\"Typed context for the pipeline.\"\"\"\n"
            "    data: dict = Field(default_factory=dict)\n"
            "    status: str = \"init\"\n\n"
            "@step(\n"
            "    name=\"process_data\",\n"
            "    version=\"v1.0\",\n"
            "    retry_count=3,\n"
            "    retry_delay=0.1,\n"
            "    tags=[\"processing\"]\n"
            ")\n"
            "class ProcessDataStep:\n"
            "    \"\"\"Professional class-based step with typed context.\"\"\"\n"
            "    def __init__(self, config_param: str = \"default\"):\n"
            "        self.config_param = config_param\n\n"
            "    @to_obj(MyContext)\n"
            "    def __call__(self, ctx: MyContext) -> Any:\n"
            "        # Your logic here\n"
            "        ctx.status = \"completed\"\n"
            "        return ctx\n"
        )

        # Main Pipeline Template
        pipeline_template = (
            "import os\n"
            "from wpipe import Pipeline\n"
            "from wpipe.exception.api_error import ProcessError\n"
            "from src.states.process_step import ProcessDataStep\n\n"
            "def create_pipeline():\n"
            "    pipeline = Pipeline(\n"
            "        pipeline_name=\"{name}\",\n"
            "        tracking_db=\"output/tracking.db\",\n"
            "        collect_system_metrics=True,\n"
            "        verbose=True\n"
            "    )\n\n"
            "    pipeline.set_steps([\n"
            "        ProcessDataStep(config_param=\"prod\")\n"
            "    ])\n"
            "    return pipeline\n\n"
            "if __name__ == \"__main__\":\n"
            "    pipeline = create_pipeline()\n"
            "    try:\n"
            "        result = pipeline.run({{\"data\": \"init\"}})\n"
            "        print(f\"Pipeline completed: {result}\")\n"
            "    except ProcessError as e:\n"
            "        print(f\"Pipeline failed: {e}\")\n"
        ).format(name=project_name)

        blueprints = {
            "requirements.txt": "wpipe>=1.0.0\nwdecorators>=2.0.0\npydantic>=2.0.0\n",
            "README.md": f"# {project_name.upper()}\n\nProfessional architecture built with **wpipe**.\n",
            "src/states/__init__.py": "from .process_step import ProcessDataStep\n",
            "src/states/process_step.py": state_template,
            "main.py": pipeline_template,
            "wpipe.config.json": '{\n  "enableBackupFile": true,\n  "maxSearchFiles": 500\n}\n'
        }

        if pipeline_type == "ai_vision_mlops":
            blueprints["requirements.txt"] += "wyolo>=1.0.0\nwtrain>=1.0.0\ncelery>=5.3.0\n"
            # Add vision specific boilerplate...
            
        return blueprints
