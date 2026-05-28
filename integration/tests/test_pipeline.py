"""
Tests for the integration pipeline (run_pipeline.py -> anonymizer -> out/).

BUG 2 (deliberate): test_output_file_exists looks for 'pipeline_out.csv' but
run_pipeline.py writes to 'pipeline_output.csv'.
Fix: change expected filename to 'pipeline_output.csv'.

BUG 3 (deliberate): mapping.json uses 'alice.smith@trading.test' and
'bob.jones@trading.test' as find targets, but fixtures contain 'alice@trading.test'
and 'bob@trading.test'. Emails are therefore NOT replaced.
Fix: update mapping.json find entries to match actual fixture emails.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_SCRIPT = REPO_ROOT / "integration" / "pipeline" / "run_pipeline.py"
OUT_DIR = REPO_ROOT / "out"


def _run_pipeline():
    return subprocess.run(
        [sys.executable, str(PIPELINE_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def test_pipeline_exits_zero():
    result = _run_pipeline()
    assert result.returncode == 0, f"Pipeline failed:\n{result.stderr}"


def test_output_file_exists():
    _run_pipeline()
    out_file = OUT_DIR / "pipeline_output.csv"
    assert out_file.exists(), (
        f"Expected output file not found: {out_file}\n"
        "Check that run_pipeline.py writes to the correct path."
    )


def test_anonymization_removes_emails():
    _run_pipeline()
    out_file = OUT_DIR / "pipeline_output.csv"
    if not out_file.exists():
        import pytest
        pytest.skip("pipeline_output.csv not present — run test_output_file_exists first")
    content = out_file.read_text(encoding="utf-8")
    # BUG 3: mapping has wrong email addresses so these will still appear in output
    assert "alice@trading.test" not in content, "trader email alice@trading.test was not anonymized"
    assert "bob@trading.test" not in content, "trader email bob@trading.test was not anonymized"


def test_anonymization_removes_names():
    _run_pipeline()
    out_file = OUT_DIR / "pipeline_output.csv"
    if not out_file.exists():
        import pytest
        pytest.skip("pipeline_output.csv not present")
    content = out_file.read_text(encoding="utf-8")
    assert "Alice Smith" not in content, "operator name 'Alice Smith' was not anonymized"
    assert "Bob Jones" not in content, "operator name 'Bob Jones' was not anonymized"
