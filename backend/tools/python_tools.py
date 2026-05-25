import tempfile
import shutil
import subprocess
import json
import os

# Get absolute path to tools in venv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_SCRIPTS = os.path.join(BASE_DIR, "..", "venv", "Scripts")

ruff_path = shutil.which("ruff") or "ruff"
bandit_path = shutil.which("bandit") or "bandit"

def run_python_static_analysis(code: str) -> list[dict]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp_path = f.name

    issues = []

    try:
        ruff_result = subprocess.run(
            [ruff_path, "check", "--output-format=json", tmp_path],
            capture_output=True, text=True
        )
        if ruff_result.stdout:
            try:
                ruff_data = json.loads(ruff_result.stdout)
                for item in ruff_data:
                    location = item.get("location", {})
                    end_location = item.get("end_location", {})
                    issues.append({
                        "rule_id": item.get("code"),
                        "description": item.get("message"),
                        "line_start": location.get("row"),
                        "line_end": end_location.get("row", location.get("row")),
                        "category": "best_practice",
                        "severity": "LOW",
                        "source": "static_analysis"
                    })
            except json.JSONDecodeError:
                pass
        bandit_result = subprocess.run([bandit_path, "-f", "json", tmp_path], capture_output=True, text=True)
        if bandit_result.stdout:
            try:
                bandit_data = json.loads(bandit_result.stdout)
                for item in bandit_data["results"]:
                    issues.append({
                        "rule_id": item.get("test_id"),
                        "description": item.get("issue_text"),
                        "line_start": item.get("line_number"),
                        "line_end": item.get("line_number"),
                        "category": "security",
                        "severity": item.get("issue_severity"),
                        "source": "static_analysis"
                    })
            except json.JSONDecodeError:
                pass

    finally:
        os.unlink(tmp_path)

    return issues