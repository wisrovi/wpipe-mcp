# Changelog

## [0.4.5] - 2026-10-27

### Added
- **WPipe Architectural Standards & QA Rules (Rules 11, 12 & 13)**:
  - **Mandatory User Inquiry & Decision Protocol (Rule 12)**: Strictly obligates AI agents and developers to NEVER make silent assumptions regarding legacy code retention or cleanup. Agents must explicitly prompt and consult the user before deleting obsolete methods/files, preserving legacy backwards-compatibility wrappers, or choosing between functionality-first vs aggressive refactoring.
  - **Exhaustive Google-Style Docstrings (Rule 2)**: Every module, class, method, and function must include complete Google-style docstrings explicitly documenting all parameters (`Args:` with types and semantic descriptions), return types and values (`Returns:`), and exceptions raised with conditions (`Raises:`). Empty or placeholder docstrings are strictly prohibited.
  - **Strict English Policy across Code and UI (Rule 1)**: Mandates 100% English across all code symbols, docstrings, comments, log messages, test names, and user interface elements (Gradio tabs, buttons, form inputs, markdown FAQs, status alerts).
  - **Strict Single Responsibility Principle (SRP) Across All Files (Rule 10)**: Clear separation of concerns enforced across microservices. View layouts must only construct UI elements, while event handlers reside in dedicated controller modules. In-memory data containers/cubes must be decoupled from file loaders, directory batch processors, and mathematical algorithms.
  - **Zero Dead Code & Redundancy (Rule 13)**: Clean repository hygiene requiring unused functions, dead code blocks, obsolete legacy wrappers, and unused imports to be removed or explicitly brought to the user's attention. Redundant duplicate files or copy-pasted services are strictly forbidden.
- **Scaffolding & Blueprint Improvements**:
  - Updated all code blueprints in `get_wpipe_architect_blueprints()` and `templates.py` to adhere to exhaustive Google-style docstrings with explicit arguments, return types, and exceptions.
  - Removed nested function closures in generated execution wrappers (`main.py`) for standard and microservice boilerplates.
- **Unit Test Coverage**:
  - Added test assertions in `tests/test_wpipe_mcp.py` verifying the presence and enforcement of Rules 1, 2, 10, 12, and 13 in `get_wpipe_architect_manual()`.

## [0.4.4] - 2026-10-22

### Added
- **WPipe QA Compliance Rules (Rules 9 & 10)**:
  - **Maximum 200 Lines Per File (Modularity & Single Responsibility)**: Enforces that no source `.py` file exceeds 200 lines. Complex business logic, heavy parsing, and utility algorithms must be decomposed into dedicated modules within `app/utils/` or `app/dto/`. Automated compliance verification added to `validate_wpipe_project()` and `optimize_wpipe_pipeline()`.
  - **Strict Single Responsibility & Zero Nested Function Closures in Steps**: WPipe `@step` classes must maintain a single, focused responsibility. Defining nested function definitions or closures inside `@step` `__call__` methods is strictly prohibited. Helper algorithms and transformations must be extracted into standalone utility functions in `app/utils/`.
- **Automated Modularity Scanning**: Added static AST inspection in `validate_wpipe_project()` to detect nested functions, reporting function names, file paths, and line numbers.
- **Unit Test Coverage**: Added dedicated test cases in `tests/test_wpipe_mcp.py` asserting detection of files > 200 lines and nested function definitions in steps.

## [0.4.3] - 2026-10-21

### Added
- **WPipe QA Compliance Rules (Rules 7 & 8)**:
  - **Zero hasattr/getattr Usage**: Dynamic reflection via `hasattr()` or `getattr()` is strictly forbidden in WPipe pipelines to guarantee type safety, predictable execution paths, and explicit Pydantic DTO contracts. Automated scanning in `validate_wpipe_project()` detects and reports line numbers and file paths of violations.
  - **Zero Bytecode Artifacts**: Project trees must contain 0 `__pycache__` directories and 0 `.pyc` compiled files to maintain clean container volumes, eliminate stale artifact bugs, and preserve repo hygiene (`PYTHONDONTWRITEBYTECODE=1`).
- **Comprehensive Agent Setup Guide**:
  - Added full install and configuration instructions for **OpenCode** (`mcp.json`), **Gemini CLI / Antigravity CLI** (`agy mcp add`), **Cursor** (MCP Settings command), and **Claude Desktop** (`claude_desktop_config.json`) in both CLI `config` helper and PyPI `README.md`.
- **Unit Test Coverage**: Added dedicated unit test cases for zero reflection and zero bytecode validation.

## [0.4.2] - 2026-10-19

### Added
- **Mandatory `app/pipelines.py` Specification**: Fully documented and formalized the mandatory role of `pipelines.py` across WPipe microservice architectures in `get_wpipe_architect_manual()`.
- **Declarative Pipeline Blueprint**: Added `Declarative Microservice Pipeline Pattern (app/pipelines.py)` in `get_wpipe_architect_blueprints()` illustrating inline step assembly with `pipeline.set_steps([...])` and typed execution helpers (`execute_<service>_pipeline()`).
- **Enhanced Scaffolding Templates**: Updated microservice scaffolding template in `templates.py` to generate `app/pipelines.py` with standalone execution helpers and structured logging.

## [0.3.1] - 2026-08-13

### Fixed
- Blueprints `\\n` literal strings replaced with real newlines (readable output).
- Ruff lint clean (`src/` and `tests/`): F403 in `src/__init__.py`, E722 bare `except` in `catalog.py`.
- Added test suite (13 tests) covering blueprints, manual, search, scaffolding, and CLI.
- Added `Makefile` with `make publish` for PyPI releases.

## [0.3.0] - 2026-06-08

### Added
- **Mandatory Attribution**: Updated the Architect's Manual and project templates to include a mandatory attribution line ("Generated by WPipe MCP by wisrovi") in all generated `README.md` files.

## [0.2.9] - 2026-06-08

### Added
- **Automated Documentation**: Added "Step 6" to the Architect's Manual (Monolith Migration Guide). It now strictly instructs AI agents to generate a professional, modern `README.md` in English, including a Mermaid flowchart diagram to visualize the resulting pipeline.

## [0.2.8] - 2026-06-08

### Fixed
- **Scaffolding and Manual Synchronization**: Updated the `deploy_wpipe_scaffolding` tool (in `templates.py`) to generate the `dto/` and `states/` folders at the root level, removing the legacy `src/` folder. This aligns the scaffolding generator with the strict architecture rules introduced in `0.2.6`, preventing AI agents from creating confusing or duplicate directory structures.

## [0.2.7] - 2026-06-08

### Added
- **Monolith Migration Guide**: MCP tools now provide a step-by-step workflow instructing agents on how to refactor monolithic scripts into WPipe architectures.
- **Strict Architecture Rules**: Enforced mandatory project structure for AI agents (`dto/` for Pydantic Contexts, `states/` for WPipe Steps, and `main.py` for the Orchestrator).
- **CLI Helper Text**: The `config` command now dynamically detects the current Python executable and prints ready-to-use installation commands for Gemini CLI and Claude Desktop.

### Fixed
- **CLI Stability**: Resolved Python syntax errors (indentation and unmatched brackets) that caused `wpipe-mcp` commands to crash.
- **Output Formatting**: Fixed literal `\n` newline characters appearing incorrectly in the CLI helper output.

## [0.2.6] - 2026-06-08

### Added
- **Strict Folder Structure Enforced**: Updated `get_wpipe_architect_blueprints` and `get_wpipe_architect_manual` tools to mandate that agents split code into `dto/`, `states/`, and `main.py`.

## [0.2.5] - 2026-06-08

### Fixed
- **CLI Config Output**: Corrected string escaping in `server.py` that caused literal `\n` characters to be printed to the terminal during `config --print`.

## [0.2.4] - 2026-06-08

### Added
- **Dynamic Python Detection**: The `wpipe-mcp config` command now uses `sys.executable` to inject the correct absolute path of the current Conda/Venv Python interpreter into the suggested `gemini mcp add` setup commands.

## [0.2.3] - 2026-06-08

### Changed
- **Enriched Agent Context**: Upgraded the `get_wpipe_architect_blueprints` tool. It now provides a concrete "Before and After" example (Monolith Migration) to help AI agents understand how to slice variables into a Pydantic `Context` object.

## [0.2.2] - 2026-06-08

### Fixed
- **Agent Handshake Prep**: Minor internal preparation in `server.py` to ensure the `run` command properly streams standard I/O for MCP discovery.

## [0.2.1] - 2026-06-08

### Added
- **Expert Blueprints Tool**: New `get_wpipe_architect_blueprints` tool providing copy-pasteable professional code for states and pipelines.

### Fixed
- **Protocol Integrity**: Forced all logging to `sys.stderr` to prevent JSON-RPC corruption on `stdout`, resolving "Invalid JSON" errors in MCP clients.
- **Redundant Logging**: Cleaned up global logging configurations in `catalog.py`.

## [0.2.0] - 2026-06-08

### Added
- **Advanced Architecture Standards**: Scaffolding now includes `timeout_sync`, `ResourceMonitor`, and `TaskTimer` for high-performance and resilient pipelines.
- **Proactive Configuration**: The `config` command now automatically creates a `.agents/wpipe-mcp.json` file in the current directory for agent auto-discovery.
- **Lazy Loading**: Improved performance by implementing lazy initialization for the steps catalog.
- **Clean CLI Output**: Added `--print` flag to `config` and silenced logs for JSON-only output.

### Changed
- **Architect's Manual (v2)**: Updated guidelines to teach agents about context managers, performance decorators, and Pydantic v2 models.
- **Resilient Boilerplate**: Templates now use `@timeout_sync` and `@to_obj(BaseModel)` as standard professional patterns.

### Fixed
- **CLI Import Error**: Resolved a critical `ModuleNotFoundError` in `__init__.py`.
- **Environment Robustness**: `config` now uses `sys.executable` to ensure path consistency across different Conda environments.

## [0.1.1] - 2026-06-07

### Fixed
- **PyPI Metadata**: Added `README.md` and complete project metadata (authors, URLs, license) for a professional appearance on PyPI.

## [0.1.0] - 2026-06-07

### Added
- **Unified CLI**: New `wpipe-mcp` command with subcommands: `run`, `start`, `stop`, `config`, and `help`.
- **Architect's Manual**: Built-in tool that provides AI agents with professional WPipe design guidelines.
- **Advanced Scaffolding**: Deploys professional project structures with Class-based states and Pydantic-typed contexts.
- **Enhanced Catalog**: Real-time synchronization with Official and Community registries (GitHub) providing namespaces and metadata.
- **Automated Installer**: `installer.sh` for easy environment setup and agent integration.

### Changed
- **Modernized Structure**: Cleaned up the repository, removed legacy `setup.py`, and adopted `pyproject.toml` standards.
- **Professional Templates**: Boilerplate now follows LTS standards for high-performance pipelines.

### Fixed
- **Catalog Reliability**: Improved fallback mechanisms for offline use.
- **Directory Management**: Safer filesystem operations during project deployment.
