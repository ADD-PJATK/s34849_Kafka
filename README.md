# s34849_Kafka — AA4: Secure AI Prompt + Mock Integration App

**Student:** s34849 — Selmane Cherifi  
**Course:** Analysis of Large Data Sets (ADD)  
**Branch:** `main` (AA4 submission) | `preaa4` (pre-AA4 backup)

---

## Quick Start — 5 commands

```bash
# 1. Install dependencies (Python 3.8+)
pip install -r mock/server/requirements.txt

# 2. Start mock server (Terminal 1)
python mock/server/server.py
# → http://localhost:8000

# 3. Open dashboard in browser (Terminal 2 or file explorer)
#    Open: mock/client-dashboard/index.html

# 4. Run integration pipeline
python integration/pipeline/run_pipeline.py
# → out/pipeline_output.csv

# 5. Run all tests
python -m pytest integration/tests/ -v
```

**Windows one-liner demo (after bugs fixed):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/demo.ps1
```

**Linux/macOS one-liner demo:**
```bash
bash scripts/demo.sh
```

---

## Repository Layout

```
s34849_Kafka/
├── README.md                           ← this file
├── .gitignore
├── documentation/
│   ├── plan-from-grading.md            ← Phase A: mock/test plan from Phase 2 feedback
│   ├── prompt.md                       ← Phase B: one-shot agent prompt (added in Phase B)
│   ├── ai-fix-log.md                   ← Phase B/C: failure evidence + fixes + reflection
│   └── ai-chat/                        ← full AI conversation export(s)
├── anonymizer/                         ← AA1: local data anonymizer (no HTTP/AI at runtime)
│   ├── anonymize.py
│   └── examples/
├── kafka-stocks/                       ← AA2: SSE stock apps (see preaa4 branch for full history)
├── mock/
│   ├── server/
│   │   ├── server.py                   ← FastAPI mock: /api/tickers, /api/latest, /api/stream
│   │   └── requirements.txt
│   ├── client-dashboard/
│   │   └── index.html                  ← browser SSE consumer + JSON/CSV export
│   └── fixtures/
│       ├── tickers.json                ← synthetic ticker list
│       └── ticks.json                  ← synthetic ticks with fictional sensitive fields
├── integration/
│   ├── pipeline/
│   │   ├── run_pipeline.py             ← fixtures → raw CSV → anonymizer → out/
│   │   └── mapping.json                ← anonymizer rules for pipeline
│   └── tests/
│       ├── test_api.py                 ← mock API tests (uses FastAPI TestClient)
│       └── test_pipeline.py            ← pipeline + anonymization tests
├── out/                                ← generated outputs (gitignored)
└── scripts/
    ├── run_mock.sh / run_mock.ps1      ← start mock server
    ├── run_tests.sh / run_tests.ps1    ← run all tests
    └── demo.sh / demo.ps1              ← end-to-end demo
```

---

## Prerequisites

| Requirement | Version |
|------------|---------|
| Python | 3.8+ |
| pip packages | `fastapi`, `uvicorn[standard]`, `httpx`, `pytest` |
| Browser | Any modern browser (for dashboard) |
| Network | **localhost only** — no external API required |

Install all Python dependencies:
```bash
pip install -r mock/server/requirements.txt
```

---

## AA1 Anonymizer (still available)

```bash
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/note.md \
  --output  out/note.anon.md
```

Full docs: [anonymizer/README.md](./anonymizer/README.md)

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'fastapi'`**
```bash
pip install -r mock/server/requirements.txt
```

**`ConnectionRefusedError` in tests or dashboard**  
The mock server is not running. Start it first:
```bash
python mock/server/server.py
```
Tests using `TestClient` do not need the server running — only live SSE tests do.

**`FileNotFoundError: out/pipeline_output.csv`**  
Run the pipeline before checking output:
```bash
python integration/pipeline/run_pipeline.py
```

**Tests fail with `AssertionError` on field names or file paths**  
This is expected before Phase B — the repo contains deliberate bugs. See `documentation/plan-from-grading.md` for the full list of anticipated failures.

**`PowerShell execution policy` blocks `.ps1` scripts**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/demo.ps1
```

---

## No Secrets Policy

- No API keys, tokens, or `.env` files are tracked in git.
- Fixtures use only synthetic / fictional data (`*.test` email domains, fictional names).
- The anonymizer makes zero network calls at runtime.
- Dashboard never stores or commits the API key.
