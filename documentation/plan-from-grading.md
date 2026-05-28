# Plan from Phase 2 Grading Feedback

**Student:** s34849 — Selmane Cherifi  
**Phase 2 feedback received:** in-class session, May 2026

---

## Phase 2 Outcome Summary

My Phase 2 submission (unified repo `s34849_Kafka`) included:

- **AA1** — Python anonymizer with working examples and screenshots.
- **AA2** — Two SSE apps (realtime dashboard + history downloader) that consumed the instructor's live API.
- **AA3** — Consolidation notes (`consolidation/CONSOLIDATION.md`).
- **AA4** — AI work plan document (`documentation/ai-work-plan.md`).

**Strengths noted:**
- Anonymizer was clean, deterministic, and well-documented.
- README covered AA1 commands accurately.
- No secrets in the repository.

**Weaknesses / deductions:**
- AA2 required an external API key and live instructor endpoint — no offline fallback.
- No automated tests for any component.
- No integration between AA1 and AA2 (data never flowed through the anonymizer).
- README had no troubleshooting section.
- No demo script proving end-to-end operation.
- SSE parsing in AA2 assumed a specific `data:` field format (`price`) without validation.

---

## Mock + Test Plan for AA4

The mock stack simulates the instructor's SSE API locally, connects to the anonymizer, and adds tests that prove both components work together.

### What is mocked

| Real component | Mock substitute |
|----------------|-----------------|
| `add.piotrkojalowicz.dev/api/tickers` | `localhost:8000/api/tickers` (from `mock/fixtures/tickers.json`) |
| `add.piotrkojalowicz.dev/api/latest` | `localhost:8000/api/latest` (from fixture file) |
| `add.piotrkojalowicz.dev/api/stream` | `localhost:8000/api/stream` (FastAPI SSE generator) |
| Live trader data with real emails | Synthetic fixtures with `alice@trading.test`, `bob@trading.test` |

### Integration pipeline

`mock/fixtures/ticks.json` → `run_pipeline.py` → `out/raw_export.csv` → **AA1 anonymizer** → `out/pipeline_output.csv`

Sensitive fields in fixtures: `trader_email`, `operator_name`, `comment`.  
Mapping file: `integration/pipeline/mapping.json`.  
Buffer size: last **20 ticks** displayed in the dashboard.

---

## Anticipated Failure Modes (≥ 5)

| # | Failure mode | Detection method |
|---|-------------|------------------|
| 1 | **Wrong field name in API response** — client or test expects `price` but server sends `lastPrice` | `pytest integration/tests/test_api.py::test_get_latest` fails with `AssertionError` |
| 2 | **Wrong output path in test** — test looks for `pipeline_out.csv` but pipeline writes `pipeline_output.csv` | `pytest integration/tests/test_pipeline.py::test_output_file_exists` fails with `AssertionError` (file not found) |
| 3 | **Anonymizer mapping mismatch** — `mapping.json` `find` list uses `alice.smith@trading.test` but fixtures contain `alice@trading.test` | `pytest integration/tests/test_pipeline.py::test_anonymization_removes_emails` fails |
| 4 | **Server not running when tests need it** — tests that make live HTTP calls start before the server is ready | `ConnectionRefusedError` in test output; fix: use FastAPI `TestClient` or add readiness wait |
| 5 | **Relative path breakage** — scripts run from wrong working directory | `FileNotFoundError` for `mock/fixtures/ticks.json`; fix: all paths use `Path(__file__).resolve()` |
| 6 | **Missing `out/` directory** — anonymizer cannot write output | `OSError: [Errno 2]`; fix: `out/` is created by `run_pipeline.py` before invoking anonymizer |

---

## Acceptance Criteria for AA4

- [ ] `python -m pytest integration/tests/ -v` → all 7 tests pass
- [ ] `python integration/pipeline/run_pipeline.py` → exits 0, `out/pipeline_output.csv` created
- [ ] `out/pipeline_output.csv` contains no raw emails (`alice@trading.test`, `bob@trading.test`)
- [ ] `out/pipeline_output.csv` contains no raw names (`Alice Smith`, `Bob Jones`)
- [ ] Mock server starts with `python mock/server/server.py` and responds on `localhost:8000`
- [ ] `GET /api/tickers` returns JSON list including `AAPL`
- [ ] `GET /api/stream?ticker=AAPL` emits `text/event-stream` events
- [ ] Dashboard (`mock/client-dashboard/index.html`) connects and shows live ticks
- [ ] No external HTTP calls at runtime; anonymizer uses no AI/LLM
