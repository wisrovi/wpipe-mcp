# Changelog

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
