import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(module)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define project name and base directory
project_name = "CustomerChurn"
base_dir = Path.cwd()

# List of required files for scaffolding
list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "Procfile",
    "research/experiments.ipynb",
    "research/trials.ipynb",
    "templates/index.html",
    "templates/result.html",
    "static/css/style.css",
    "static/js/script.js",
]

def create_project_structure(files):
    """Creates directories and files based on the given list."""
    for file_path in files:
        file_path = base_dir / Path(file_path)
        directory = file_path.parent

        # Create directory if it doesn't exist
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

        # Create file if it doesn't exist or is empty
        if not file_path.exists() or file_path.stat().st_size == 0:
            file_path.touch()
            logger.info(f"Created empty file: {file_path}")
        else:
            logger.info(f"File already exists: {file_path}")

if __name__ == "__main__":
    logger.info(f"Starting project scaffolding for: {project_name}")
    create_project_structure(list_of_files)
    logger.info("Project scaffolding completed successfully.")
