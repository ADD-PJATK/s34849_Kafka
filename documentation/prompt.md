# Phase B — One-Shot Agent Prompt

> Paste the text below verbatim into your AI coding agent (Cursor Agent, Claude Code, etc.).

---

## PROMPT START

You are fixing a broken Python mock-stock integration stack in the repo `s34849_Kafka` (branch `main`). The repo is fully offline — no external APIs, no secrets. Your job is to find and fix all failing tests, verify the end-to-end pipeline works, and update `documentation/ai-fix-log.md` with evidence.

---

### Stack

- Python 3.8+ (standard library + fastapi, uvicorn, httpx, pytest)
- No external network calls at runtime
- All paths use `Path(__file__).resolve()` — do NOT hardcode working-directory-relative paths

---

### Repository layout (key paths)

```
s34849_Kafka/
├── mock/
│   ├── server/server.py          ← FastAPI: GET /api/tickers, /api/latest, GET /api/stream (SSE)
│   ├── server/requirements.txt   ← fastapi, uvicorn, httpx, pytest
│   ├── client-dashboard/index.html
│   └── fixtures/
│       ├── tickers.json          ← ["AAPL","GOOG","MSFT","TSLA","AMZN"]
│       └── ticks.json            ← array of ticks; fields include lastPrice, trader_email, operator_name
├── integration/
│   ├── pipeline/
│   │   ├── run_pipeline.py       ← reads ticks.json → writes raw CSV → runs anonymizer → out/pipeline_output.csv
│   │   └── mapping.json          ← anonymizer replacement rules
│   └── tests/
│       ├── test_api.py           ← uses FastAPI TestClient (no live server needed)
│       └── test_pipeline.py      ← runs run_pipeline.py as subprocess, checks out/ files
├── anonymizer/anonymize.py       ← AA1: deterministic string replacer, no HTTP/AI at runtime
│                                    CLI: python anonymize.py --mapping FILE --input FILE --output FILE
└── out/                          ← generated; created by run_pipeline.py
```

---

### Install and run commands

```bash
# Install dependencies (run from repo root)
pip install -r mock/server/requirements.txt

# Start mock server (Terminal 1)
python mock/server/server.py
# → listens on http://localhost:8000

# Run integration pipeline (Terminal 2 or standalone)
python integration/pipeline/run_pipeline.py
# → creates out/raw_export.csv and out/pipeline_output.csv

# Run all tests
python -m pytest integration/tests/ -v

# Full end-to-end demo (Windows)
powershell -ExecutionPolicy Bypass -File scripts/demo.ps1
# Full end-to-end demo (Linux/macOS)
bash scripts/demo.sh
```

---

### What "done" looks like — acceptance checklist

- [ ] `python -m pytest integration/tests/ -v` → **all 8 tests pass**, 0 failures
- [ ] `python integration/pipeline/run_pipeline.py` → exits 0; `out/pipeline_output.csv` exists
- [ ] `out/pipeline_output.csv` does NOT contain `alice@trading.test` or `bob@trading.test`
- [ ] `out/pipeline_output.csv` does NOT contain `Alice Smith` or `Bob Jones`
- [ ] `GET http://localhost:8000/api/tickers` → JSON list including `"AAPL"`
- [ ] `GET http://localhost:8000/api/latest?ticker=AAPL` → JSON object with `"lastPrice"` key
- [ ] `GET http://localhost:8000/api/stream?ticker=AAPL` → `text/event-stream` response with `data:` lines
- [ ] No external HTTP calls made at any point; anonymizer uses no AI/LLM

---

### Debugging playbook — start here

**Step 1 — run tests and read failures carefully:**
```bash
python -m pytest integration/tests/ -v
```
Expect 3 failures. Each failure message names the exact assertion and the actual vs expected value.

**Step 2 — for API test failures (`test_api.py`):**
- Open `mock/server/server.py` and `mock/fixtures/ticks.json`
- Check what field names the fixtures use (e.g. `lastPrice` vs `price`)
- Check what the test assertions expect
- Fix the mismatch in the test OR in the server — whichever is semantically correct

**Step 3 — for pipeline test failures (`test_pipeline.py`):**
- Check what filename `run_pipeline.py` writes to (`OUT_FILE` variable)
- Check what filename the test looks for (the `out_file` variable in the failing test)
- Fix the mismatch

**Step 4 — for anonymization failures (`test_anonymization_removes_emails`):**
- Open `integration/pipeline/mapping.json`
- Open `mock/fixtures/ticks.json` — look at the actual `trader_email` values
- Compare the `find` arrays in the mapping with the actual email strings in fixtures
- Update the `find` entries to match the exact email strings used in the fixtures

**Step 5 — re-run tests to confirm all pass:**
```bash
python -m pytest integration/tests/ -v
```

**Step 6 — run the full pipeline manually and inspect output:**
```bash
python integration/pipeline/run_pipeline.py
cat out/pipeline_output.csv   # or type out\pipeline_output.csv on Windows
```
Verify emails and names are replaced with `[EMAIL_REDACTED]` and `[PERSON_REDACTED]`.

---

### Safety constraints (mandatory — do not violate)

- Do NOT add any API keys, tokens, passwords, or `.env` files
- Do NOT make any HTTP calls to external hosts — localhost only
- Do NOT call any AI/LLM service from within the anonymizer or pipeline at runtime
- Do NOT rewrite files unrelated to the failing tests
- The anonymizer (`anonymizer/anonymize.py`) must remain deterministic string replacement only

---

### Scope — fix only what is broken

Make the **minimal changes** needed to pass all 8 tests:
- Fix field name mismatches between fixtures/server and test assertions
- Fix the output filename mismatch in the pipeline test
- Fix the email `find` entries in `integration/pipeline/mapping.json`
- Do not refactor, rename, or restructure unrelated code

---

### After all tests pass — update the fix log

Write `documentation/ai-fix-log.md` with:
1. The initial test failure output (copy from terminal)
2. A bullet summary of each fix (file changed, what was wrong, what you changed)
3. The final passing test output (copy from terminal)
4. 5–10 sentences reflecting on what you learned about prompting and debugging this kind of integration

## PROMPT END
