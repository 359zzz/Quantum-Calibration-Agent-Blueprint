"""Find tool for locating files and directories."""

import subprocess
from pathlib import Path
from langchain_core.tools import tool


@tool
def find(
    path: str = ".",
    name: str = "",
    type: str = "",
    maxdepth: int = 10,
) -> dict:
    """Find files or directories matching criteria.

    Args:
        path: Directory to search in (default: current directory)
        name: Name pattern to match (supports wildcards like *.py)
        type: Type filter - 'f' for files, 'd' for directories
        maxdepth: Maximum directory depth to search (default: 10)

    Returns:
        dict with 'matches' list of found paths, or 'error' on failure
    """
    cmd = ["find", path, "-maxdepth", str(maxdepth)]

    if name:
        cmd.extend(["-name", name])

    if type:
        cmd.extend(["-type", type])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return {"error": result.stderr.strip() or "Find command failed"}

        matches = [line for line in result.stdout.strip().split("\n") if line]
        return {"matches": matches, "count": len(matches)}

    except subprocess.TimeoutExpired:
        return {"error": "Find command timed out after 30 seconds"}
    except Exception as e:
        return {"error": str(e)}
