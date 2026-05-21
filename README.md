# s34849_Kafka — ADD Project (Phase 2)

**Student:** s34849 — Selmane Cherifi  
**Course:** Analysis of Large Data Sets (ADD)  
**Branch:** `main`

This repository contains all additional assignments for Phase 2, unified in a single repo per the Phase 2 specification.

| Path | Assignment | Description |
|------|------------|-------------|
| [`anonymizer/`](./anonymizer/) | AA1 | Local Data Anonymizer — Python CLI, no external APIs |
| [`kafka-stocks/realtime-dashboard/`](./kafka-stocks/realtime-dashboard/) | AA2 App 1 | Real-time stock price dashboard via Kafka / SSE |
| [`kafka-stocks/history-downloader/`](./kafka-stocks/history-downloader/) | AA2 App 2 | Stock history collector with CSV/JSON export |
| [`documentation/ai-work-plan.md`](./documentation/ai-work-plan.md) | AA4 | AI-assisted work plan document |
| [`consolidation/CONSOLIDATION.md`](./consolidation/CONSOLIDATION.md) | AA3 | Merge notes — two repos unified here |

---

## Quick Start — AA1: Local Data Anonymizer

**Requirements:** Python 3.8+ (standard library only — no `pip install` needed)

```bash
# Anonymize a Markdown file
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/note.md \
  --output  out/note.anon.md

# Anonymize a CSV file
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/records.csv \
  --output  out/records.anon.csv

# Anonymize a plain-text log
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/log.txt \
  --output  out/log.anon.txt

# Anonymize a JSON data file
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/data.json \
  --output  out/data.anon.json

# Dry run — preview replacements without writing output
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/note.md \
  --output  out/note.anon.md \
  --dry-run
```

> **No external APIs or AI/LLM services are used at runtime.** All replacements are deterministic local string substitutions using only the Python standard library.

Full documentation: [`anonymizer/README.md`](./anonymizer/README.md)

---

## Quick Start — AA2: Real-time Stock Data (Kafka / SSE)

**Requirements:** Python 3, any modern browser, API key from `https://add.piotrkojalowicz.dev/`

```bash
# Terminal 1 — start the local CORS proxy (required for browser SSE)
python kafka-stocks/proxy_server.py

# Terminal 2 — serve the app files
python -m http.server 8080 --directory kafka-stocks
```

Then open in your browser:

| App | URL | Description |
|-----|-----|-------------|
| App 1 — Realtime Dashboard | `http://localhost:8080/realtime-dashboard/` | Live price stream, sparkline charts |
| App 2 — History Downloader | `http://localhost:8080/history-downloader/` | Accumulates ticks, CSV/JSON export |

Enter your API key in the UI form — it is **never stored in any file or committed to git**.

Screenshots: [`kafka-stocks/realtime-dashboard/screenshots/`](./kafka-stocks/realtime-dashboard/screenshots/) and [`kafka-stocks/history-downloader/screenshots/`](./kafka-stocks/history-downloader/screenshots/)

---

## Repository Layout

```
s34849_Kafka/
├── README.md                               ← this file
├── .gitignore
├── anonymizer/                             ← AA1: Local Data Anonymizer
│   ├── README.md                           ← prerequisites, install, run, mapping format
│   ├── anonymize.py                        ← CLI tool (no HTTP/LLM at runtime)
│   ├── examples/
│   │   ├── mapping.json                    ← 6-rule mapping (names, emails, phone, address)
│   │   ├── note.md
│   │   ├── records.csv
│   │   ├── log.txt
│   │   ├── data.json
│   │   └── output/                         ← pre-generated anonymized outputs (all 4 types)
│   └── screenshots/                        ← terminal run screenshots (.md and .csv runs)
├── kafka-stocks/                           ← AA2: Real-time Stock Data
│   ├── proxy_server.py                     ← shared CORS proxy (port 8765, run first)
│   ├── realtime-dashboard/                 ← App 1: live SSE price stream
│   │   ├── index.html
│   │   ├── README.md
│   │   └── screenshots/
│   └── history-downloader/                 ← App 2: tick history + CSV/JSON export
│       ├── index.html
│       ├── README.md
│       └── screenshots/
├── documentation/
│   └── ai-work-plan.md                     ← AA4: AI-Assisted Work Plan (Selmane Cherifi)
└── consolidation/
    └── CONSOLIDATION.md                    ← AA3: merge notes (two repos → one)
```

---

## No Secrets Policy

- API keys are entered at runtime in the browser UI form only.
- No `.env` files, tokens, or credentials are tracked in git.
- The anonymizer tool makes zero network calls at runtime.
