"""System prompt loader with runtime injection."""

import platform
from datetime import datetime
from pathlib import Path

# Root directory (where this file lives)
ROOT_DIR = Path(__file__).parent

# Data directories
DATA_DIR = ROOT_DIR / "data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
EXPERIMENTS_DIR = DATA_DIR / "experiments"
WORKFLOWS_DIR = DATA_DIR / "workflows"

# Knowledge subdirectories
SKILLS_DIR = KNOWLEDGE_DIR / "skills"
DOCUMENTS_DIR = KNOWLEDGE_DIR / "documents"
MEMORY_DIR = KNOWLEDGE_DIR / "memory"

# Scripts directory
SCRIPTS_DIR = ROOT_DIR / "scripts"

# Config
CONFIG_PATH = ROOT_DIR / "config.yaml"


def load_system_prompt() -> str:
    """Load system prompt and inject runtime values."""
    prompt_file = KNOWLEDGE_DIR / "system-prompt.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"System prompt not found: {prompt_file}")

    template = prompt_file.read_text(encoding="utf-8")

    # Detect platform/shell
    system = platform.system()
    if system == "Windows":
        platform_str = "Windows"
        shell_str = "PowerShell / cmd"
    elif system == "Darwin":
        platform_str = "macOS"
        shell_str = "bash / zsh"
    else:
        platform_str = f"Linux ({platform.release().split('-')[0]})"
        shell_str = "bash"

    # Inject runtime values (use relative paths for virtual filesystem compatibility)
    replacements = {
        "{{DATETIME}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "{{PLATFORM}}": platform_str,
        "{{SHELL}}": shell_str,
        "{{SCRIPTS_DIR}}": str(SCRIPTS_DIR.relative_to(ROOT_DIR)),
        "{{SKILLS_DIR}}": str(SKILLS_DIR.relative_to(ROOT_DIR)),
        "{{DOCUMENTS_DIR}}": str(DOCUMENTS_DIR.relative_to(ROOT_DIR)),
        "{{MEMORY_DIR}}": str(MEMORY_DIR.relative_to(ROOT_DIR)),
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return template
