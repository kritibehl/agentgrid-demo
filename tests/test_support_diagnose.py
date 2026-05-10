import json
import subprocess


def test_support_diagnose_cli():
    result = subprocess.run(
        [
            "python3",
            "-m",
            "src.support.diagnose",
            "--case",
            "examples/tool_failure_case.json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)

    assert data["issue_type"] == "tool_failure"
    assert data["decision"] == "escalate"
    assert "trace_" in data["trace_id"]
