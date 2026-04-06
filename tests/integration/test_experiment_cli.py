"""E2E tests for experiment CLI commands."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLI_PATH = PROJECT_ROOT / "cli.py"


class TestExperimentsRunCommand:
    """E2E tests for 'experiments run' command."""

    def test_run_json_output(self, temp_scripts_dir, temp_data_dir):
        """Test JSON output contains experiment results."""
        result = subprocess.run(
            [
                sys.executable, str(CLI_PATH),
                "experiments", "run", "test_experiment",
                "-p", json.dumps({"param1": 5.0}),
            ],
            capture_output=True,
            text=True,
            env={
                **subprocess.os.environ,
                "QCAL_SCRIPTS_DIR": str(temp_scripts_dir),
                "QCAL_DATA_DIR": str(temp_data_dir),
            },
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        output = json.loads(result.stdout)
        assert output["status"] == "success"

    def test_run_preserves_results(self, temp_scripts_dir, temp_data_dir):
        """Results from experiment 'data' field should be saved, not discarded."""
        result = subprocess.run(
            [
                sys.executable, str(CLI_PATH),
                "experiments", "run", "test_experiment",
                "-p", json.dumps({"param1": 5.0}),
            ],
            capture_output=True,
            text=True,
            env={
                **subprocess.os.environ,
                "QCAL_SCRIPTS_DIR": str(temp_scripts_dir),
                "QCAL_DATA_DIR": str(temp_data_dir),
            },
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        output = json.loads(result.stdout)
        assert output["results"] != {}, "Experiment results should not be empty"
        assert "result" in output["results"], "Expected 'result' key in results"

    def test_run_human_output(self, temp_scripts_dir, temp_data_dir):
        """Test human-readable output format."""
        result = subprocess.run(
            [
                sys.executable, str(CLI_PATH),
                "experiments", "run", "test_experiment",
                "-p", json.dumps({"param1": 5.0}),
                "-h",
            ],
            capture_output=True,
            text=True,
            env={
                **subprocess.os.environ,
                "QCAL_SCRIPTS_DIR": str(temp_scripts_dir),
                "QCAL_DATA_DIR": str(temp_data_dir),
            },
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert "Experiment ID:" in result.stdout
        assert "Status:" in result.stdout

    def test_run_invalid_experiment(self, temp_scripts_dir, temp_data_dir):
        """Test running a non-existent experiment."""
        result = subprocess.run(
            [
                sys.executable, str(CLI_PATH),
                "experiments", "run", "nonexistent_experiment",
                "-p", "{}",
            ],
            capture_output=True,
            text=True,
            env={
                **subprocess.os.environ,
                "QCAL_SCRIPTS_DIR": str(temp_scripts_dir),
                "QCAL_DATA_DIR": str(temp_data_dir),
            },
        )
        assert result.returncode != 0 or "error" in result.stdout.lower() or "not found" in result.stdout.lower()
