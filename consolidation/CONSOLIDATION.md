# Consolidation Notes

**Student:** s34849  
**Date:** 2026-05-21  
**Target repository:** `ADD-PJATK/s34849_Kafka`

---

## Situation

Student s34849 originally maintained two separate repositories:

| Repository | Account | Contents |
|------------|---------|----------|
| `Selmanepj/ADD_s34849_Kafka_task` | Personal GitHub | AA2 — Real-time Stock Data (Kafka / SSE) |
| `Selmanepj/s34849__anonymizer` | Personal GitHub | AA1 — Local Data Anonymizer |

The Phase 2 specification requires both AA1 and AA2 to live in **one** repository named `s34849_Kafka` under the ADD-PJATK GitHub organisation on `main`. This document records all merge actions taken.

---

## Actions Taken

### AA2 — Kafka / SSE apps (from `ADD_s34849_Kafka_task`)

1. `app1-dashboard/` was renamed to `kafka-stocks/realtime-dashboard/` to match the required layout.
2. `app2-history/` was renamed to `kafka-stocks/history-downloader/`.
3. `proxy_server.py` was placed at `kafka-stocks/proxy_server.py` (shared by both apps).
4. Per-app READMEs were updated: proxy path corrected to `python kafka-stocks/proxy_server.py`; open URLs updated to `/realtime-dashboard/` and `/history-downloader/`.

### AA1 — Anonymizer (from `Selmanepj/s34849__anonymizer`)

5. All AA1 source files placed under `anonymizer/`:
   - `anonymize.py` → `anonymizer/anonymize.py`
   - `examples/` → `anonymizer/examples/`
   - `screenshots/` → `anonymizer/screenshots/`
   - AA1 README → `anonymizer/README.md`

### New files added

6. Root `README.md` replaced with a unified repo map and quick-start commands for AA1 and AA2.
7. `documentation/ai-work-plan.md` (AA4) added.
8. `consolidation/CONSOLIDATION.md` (this file) added.
9. `.gitignore` updated to cover Python, Node.js/npm, Kafka/Java, Spark, and environment files.

---

## Verification Checklist

```bash
# AA1 — anonymizer must run from repo root
python anonymizer/anonymize.py \
  --mapping anonymizer/examples/mapping.json \
  --input   anonymizer/examples/note.md \
  --output  out/note.anon.md
# Expected: "Done. N replacement(s) applied -> out/note.anon.md"

# AA2 — proxy must start without errors
python kafka-stocks/proxy_server.py
# Expected: listening message on localhost

# Security — no secrets in tracked files
git grep -i "api_key\|password\|secret\|token" -- "*.py" "*.json" "*.md" "*.html"
# Expected: no real credential values

# Anonymizer must not import networking libraries
grep -n "^import\|^from" anonymizer/anonymize.py
# Expected: only argparse, json, re, sys, pathlib
```

---

## Result

All AA1 and AA2 files are on `main` in `ADD-PJATK/s34849_Kafka` with the correct subfolder layout per the Phase 2 specification. Both AA1 and AA2 are documented in the root `README.md`. No API keys or secrets are committed.
