import json
import subprocess
from copy import deepcopy
from pathlib import Path
from shutil import rmtree
from typing import Dict

import pytest

THIS_DIR = Path(__file__).parent
PROJECT_DIR = (THIS_DIR / "../").resolve()

@pytest.fixture(scope="session")
def project_dir():
    template_values = {
        "repo_name": "test-repo",
    }
    generate_repo_dir: Path = generate_project(template_values=template_values)
    yield generate_repo_dir
    rmtree(generate_repo_dir, ignore_errors=True)
    

def generate_project(template_values: Dict[str, str]):
    template_values: Dict[str, str] = deepcopy(template_values)
    cookiecutter_config = {
        "default_context": template_values
    }
    cookiecutter_config_fpath = PROJECT_DIR / "cookiecutter_test_config.json"
    cookiecutter_config_fpath.write_text(json.dumps(cookiecutter_config))
    cmd = [
        "cookiecutter",
        str(PROJECT_DIR),
        "--output-dir",
        str(PROJECT_DIR / "sample"),
        "--no-input",
        "--config-file",
        str(cookiecutter_config_fpath),
        "--verbose"
    ]
    subprocess.run(cmd, check=True)

    generate_repo_dir = PROJECT_DIR / "sample" / template_values["repo_name"]
    return generate_repo_dir


def test__can_generate_project(project_dir: Path):
    """
    execute: `cookiecutter <template directory> ...`
    """

    assert project_dir.exists()
    
    
