# AI Fix Log — AA4 Phase B

**Agent:** Claude Code (claude-sonnet-4-6)  
**Date:** 2026-05-28  
**Prompt:** `documentation/prompt.md`

---

## Initial failure output

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
collected 8 items

integration/tests/test_api.py::test_get_tickers PASSED
integration/tests/test_api.py::test_get_latest FAILED
integration/tests/test_api.py::test_get_latest_unknown_ticker PASSED
integration/tests/test_api.py::test_tickers_not_empty PASSED
integration/tests/test_pipeline.py::test_pipeline_exits_zero PASSED
integration/tests/test_pipeline.py::test_output_file_exists FAILED
integration/tests/test_pipeline.py::test_anonymization_removes_emails FAILED
integration/tests/test_pipeline.py::test_anonymization_removes_names PASSED

FAILED test_api.py::test_get_latest
  AssertionError: Expected 'price' key in tick response
  assert 'price' in {'lastPrice': 179.1, 'ticker': 'AAPL', ...}

FAILED test_pipeline.py::test_output_file_exists
  AssertionError: Expected output file not found: out\pipeline_out.csv

FAILED test_pipeline.py::test_anonymization_removes_emails
  AssertionError: trader email alice@trading.test was not anonymized
  'alice@trading.test' still present in out/pipeline_output.csv

3 failed, 5 passed in 0.96s
```

---

## Fixes applied

### Fix 1 — `integration/tests/test_api.py` (Bug 1: wrong field name)

**What was wrong:** `test_get_latest` asserted `"price" in tick` but the server and fixtures consistently use `"lastPrice"`.

**Change:** Line 34 — `assert "price" in tick` → `assert "lastPrice" in tick`

---

### Fix 2 — `integration/tests/test_pipeline.py` (Bug 2: wrong output filename)

**What was wrong:** `test_output_file_exists` looked for `out/pipeline_out.csv` but `run_pipeline.py` writes to `out/pipeline_output.csv`.

**Change:** Line 38 — `OUT_DIR / "pipeline_out.csv"` → `OUT_DIR / "pipeline_output.csv"`

---

### Fix 3 — `integration/pipeline/mapping.json` (Bug 3: mismatched email patterns)

**What was wrong:** The `find` entries used `alice.smith@trading.test` and `bob.jones@trading.test` but the fixtures (`mock/fixtures/ticks.json`) contain `alice@trading.test` and `bob@trading.test`. The anonymizer found zero matches, leaving raw emails in the output CSV.

**Change:** Updated both find arrays:
- `"alice.smith@trading.test"` → `"alice@trading.test"`
- `"bob.jones@trading.test"` → `"bob@trading.test"`

---

## Final passing output

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
collected 8 items

integration/tests/test_api.py::test_get_tickers PASSED             [ 12%]
integration/tests/test_api.py::test_get_latest PASSED              [ 25%]
integration/tests/test_api.py::test_get_latest_unknown_ticker PASSED [ 37%]
integration/tests/test_api.py::test_tickers_not_empty PASSED       [ 50%]
integration/tests/test_pipeline.py::test_pipeline_exits_zero PASSED [ 62%]
integration/tests/test_pipeline.py::test_output_file_exists PASSED  [ 75%]
integration/tests/test_pipeline.py::test_anonymization_removes_emails PASSED [ 87%]
integration/tests/test_pipeline.py::test_anonymization_removes_names PASSED [100%]

======================== 8 passed, 1 warning in 0.88s =========================
```

Pipeline output (`out/pipeline_output.csv`) confirmed: no raw emails or names remain.

---

## Reflection

The one-shot prompt worked because it gave the agent a precise debugging playbook rather than a vague instruction. By naming the exact files to compare (fixtures vs. test assertions), the agent could pinpoint each mismatch without exploring irrelevant code. The three bugs were intentionally small and bounded — a wrong key name, a wrong filename, a wrong string in a config — which is exactly the kind of error that benefits from structured prompting: tell the agent *where* to look and *what* to compare, not just *what* to fix. Writing the prompt forced me to deeply understand the system before the session, which is itself a valuable engineering exercise. I also learned that anonymizer failures are silent by default — the tool exits 0 even when zero replacements happen, so tests must explicitly assert absence of sensitive strings rather than trusting the tool ran. For future projects, I would add a warning or nonzero exit when a mapping produces zero matches, making this class of bug self-detecting. The FastAPI TestClient approach (no live server) made API tests fast and deterministic — a pattern worth carrying into any SSE-based project. Overall, a well-structured prompt with explicit acceptance criteria is more valuable than a long description of the bug, because it gives the agent a reproducible verification step after each fix.
