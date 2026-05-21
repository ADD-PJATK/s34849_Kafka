# AI-Assisted Work Plan – ADD Project

**Document title:** AI-Assisted Work Plan – ADD Project  
**Student ID:** s34849  
**Date last updated:** 2026-05-21  
**Course:** Analysis of Large Data Sets (ADD)  
**Repository:** [s34849_kafka](https://github.com/selmanepj/s34849_kafka)

---

## 3.2 Scope of AI Use in This Project

The table below defines where AI assistance is permitted and where it is explicitly prohibited across all ADD project tasks, including AA1 and AA2.

| Activity | Allowed? | Notes |
|----------|----------|-------|
| Boilerplate code, CLI scaffolding | **Yes** | Acceptable for skeleton files; every generated line must be reviewed and tested locally |
| PySpark / Spark transformations | **Yes** | Must verify against PySpark 3.x official documentation before committing |
| Writing task reports (`documentation/taskNN_*.md`) | **Yes – with edits** | AI drafts; student verifies all facts, corrects inaccuracies, and rewrites in own words |
| Debugging error messages | **Yes** | Sanitize stack traces before pasting; never include credentials or real personal data |
| Designing architecture diagrams | **Yes** | Mermaid or ASCII; must reflect actual implementation, not aspirational design |
| Kafka consumer/producer boilerplate | **Yes** | Must be tested end-to-end with a real broker before any commit |
| Data schema and transformation logic | **Yes – review required** | Validate output samples against expected schema on real or synthetic data |
| **Runtime anonymization (AA1 tool)** | **No** | Per AA1 spec: zero HTTP or LLM calls at runtime; purely local Python standard library |
| Submitting unreviewed AI output | **No** | AI output must always be read, tested, and edited by the student before any commit |
| Exam, quiz, or individually assessed work | **No** | Per ADD course academic integrity policy |

---

## 3.3 Tools and Models

The following AI tools are used or planned for this ADD project:

### Claude (Anthropic) – Claude Sonnet 4.6
- **Interface:** Claude.ai web UI and Claude Code CLI extension for VS Code
- **Use cases:** Architecture discussions, code review, drafting documentation, explaining PySpark APIs, debugging sanitized error messages, generating the initial draft of this document
- **Data handling:** Cloud-based. Prompts may be used to improve Anthropic models unless the user opts out via account settings. Do not paste real personal data, API keys, or `.env` contents. Governed by Anthropic's privacy policy.

### GitHub Copilot
- **Interface:** VS Code inline completion extension
- **Use cases:** Python boilerplate completions, Kafka producer/consumer patterns, small function bodies
- **Data handling:** Cloud-based (Microsoft / GitHub servers). Code context is sent for each completion. Never type credentials or real personal data in files open in Copilot sessions.

### ChatGPT (OpenAI) – GPT-4o
- **Interface:** ChatGPT web UI
- **Use cases:** Exploratory concept questions (Kafka internals, SSE protocol, Spark shuffle), sanity-checking algorithmic approaches
- **Data handling:** Cloud-based. Do not upload real datasets or paste schemas containing real user data. Use public-domain or synthetic samples only.

### Local fallback
- When network AI tools are unavailable: use Python REPL, `pydoc`, PySpark shell, and official documentation (`spark.apache.org`, `kafka.apache.org`) directly.

---

## 3.4 Standard Workflow (Step-by-Step)

The following six-step workflow is applied consistently whenever AI assistance is requested for any ADD task.

**Step 1 — Write a short human spec before opening any AI chat.**  
Define the goal, inputs, outputs, and hard constraints in plain English before asking AI anything. Example: "Script must read raw JSON from `data/stocks/raw/`, write Parquet partitioned by `date` to `data/stocks/parquet/`, using PySpark 3.5, Python 3.11, no external network calls." This spec is pasted verbatim into the prompt so the AI has the full picture.

**Step 2 — Paste only the minimum necessary context.**  
Include only the relevant file excerpt, sanitized error message, or schema definition. Never paste the entire repository, a `.env` file, real personal data, or API keys. If a schema example is needed, use column names from a synthetic or public-domain sample.

**Step 3 — Ask for a plan before code.**  
Request a numbered approach (data flow, edge cases, dependencies) and confirm it satisfies the task's acceptance criteria before asking for any implementation. This prevents wasted effort on approaches that violate course requirements or the AA1 no-API runtime rule.

**Step 4 — Generate code, then review every line before running.**  
Read the generated code top-to-bottom. Verify: all imports exist in the project environment, file paths match the repository layout, no hard-coded credentials, error handling covers empty input and missing files. Run the script on `examples/` or synthetic data locally before accepting any change.

**Step 5 — Test against the task acceptance checklist.**  
Run through every checkbox in the relevant `ACCEPTANCE.md` section before committing. For the anonymizer: verify `anonymizer/examples/mapping.json` + a sample input produce the documented output. For the Kafka apps: verify data flows through the broker and appears in the dashboard/output file. Capture a screenshot as evidence.

**Step 6 — Commit with a precise, descriptive message.**  
Write a commit message describing what changed and why. Example: `feat(anonymizer): move source into anonymizer/ subfolder for unified repo`. Never use messages like "AI fix" or "update code." The commit message is the permanent record of intent and will be read by the instructor.

---

## 3.5 Prompting Rules (What to Always Include in Prompts)

The following ten rules are applied to every prompt sent to an AI tool on this project:

- **Always name the file path and language/stack.** E.g., "In `anonymizer/anonymize.py`, Python 3.11, standard library only — no `pip install` packages."
- **State course constraints explicitly.** E.g., "This script must not make any HTTP, HTTPS, or external API calls at runtime. This is a hard requirement of the AA1 specification."
- **Ask for idempotent scripts with explicit run instructions.** Every generated script must include a `if __name__ == '__main__':` guard and a copy-pasteable CLI example that works from the repository root.
- **Require error handling for missing files and empty datasets.** Generated code must handle `FileNotFoundError`, empty DataFrames, malformed JSON, and non-UTF-8 input without silent failures or unhandled exceptions.
- **Forbid invented libraries or APIs.** Include: "Use only libraries available in this environment: Python 3.11 standard library / PySpark 3.5 / confluent-kafka 2.x. If you are unsure whether a function or class exists, say so explicitly rather than guessing."
- **Ask for diff-style or minimal changes when editing existing files.** "Show only the changed lines with before/after context, not the full file, to make review fast."
- **Include the relevant acceptance criteria from the task spec in the prompt.** Paste the checklist items directly so the AI generates code that addresses graded requirements, not hypothetical ones.
- **Specify the exact output format.** E.g., "Return one Markdown code block containing the full file, then a second block with the exact CLI command to run it."
- **Request explanations for non-obvious logic.** "After the code block, add a short paragraph explaining any line that uses a non-obvious pattern, regex, or Spark API."
- **End every prompt with:** "If any requirement is ambiguous or if you are unsure whether a library, flag, or API exists, ask a clarifying question before writing code."

---

## 3.6 Precautions and Prohibited Uses

The following rules govern all AI use on this project. **All rules are mandatory and non-negotiable.**

1. **Secrets — must never be pasted into AI tools.** API keys, passwords, `.env` file contents, Kafka broker credentials, cloud storage access keys, and any other secrets must never appear in prompts or file attachments. If debugging a configuration issue, replace all credential values with `***REDACTED***` before pasting.

2. **Personal data — must not be uploaded or shared.** Do not paste, upload, or reference real personal data in any AI tool. Use only synthetic datasets (e.g., `anonymizer/examples/mapping.json` with fictional names) or clearly public-domain data in all prompts.

3. **Verification before merge — AI output must be run, not just read.** Never merge or commit AI-generated code purely because it "looks correct." Every generated script must execute successfully on at least one real or synthetic input locally before it is staged.

4. **Hallucination check — verify all APIs, flags, and class names.** AI models regularly invent parameter names, deprecated APIs, and non-existent configuration keys. Before using any Spark, Kafka, or CLI flag generated by AI, cross-check it against the official documentation (`spark.apache.org`, `kafka.apache.org`, `docs.confluent.io`).

5. **Licence and attribution — note AI-generated blocks in reports.** When a substantial block of code is AI-generated and committed verbatim, note it in the task report or commit message. This is required for academic integrity and does not reduce the grade.

6. **Repo consistency — AI must not rewrite unrelated files.** If an AI response modifies files outside the current task scope (e.g., changes `kafka-stocks/` during an `anonymizer/` task), revert those changes immediately with `git checkout -- <file>` before staging anything.

7. **Scope creep — AI must not add unrequested features.** AI tools frequently add logging frameworks, config files, or unit-test scaffolding not requested in the spec. Accept only what the acceptance checklist requires. Remove anything extra before committing.

8. **Testing evidence — keep proof that the pipeline ran.** Retain terminal screenshots, sample output files, or log excerpts in `screenshots/` for each deliverable. Do not delete evidence files after submission; they may be requested during a viva.

9. **Academic integrity — the student is responsible for the work.** AI is a tool for learning and productivity. The student must be able to explain, defend, and modify every line of committed code. If a section cannot be explained without re-reading the AI output, rewrite it until it is understood.

10. **No AI in the anonymizer runtime path.** The AA1 tool (`anonymizer/anonymize.py`) must perform all replacements using local Python string operations. It must not import `requests`, `openai`, `anthropic`, `httpx`, or any other networking library. This is verified by reading the import list before every commit.

11. **No AI for exam or individual assessment tasks.** Any task explicitly marked as individual assessment, quiz, or exam by the instructor must be completed without AI assistance, regardless of how other tasks are handled.

12. **Stop using AI when:** debugging involves real production data with personal information; the problem requires knowledge of internal infrastructure not in public documentation; any prompt would require exposing live secrets; or the student is preparing for an oral defence where the work must be independently reproducible from memory.

---

## 3.7 Task-Specific AI Plans (ADD Project)

### AA1 — Local Data Anonymizer

**What AI will help with:**
- Drafting the `re.escape` + `re.IGNORECASE` pattern for case-insensitive replacement
- Reviewing argparse CLI argument definitions for clarity
- Writing error message copy in clear English

**What I will do without AI:**
- Define the mapping JSON schema and validation rules from scratch
- Manually test all edge cases: overlapping `find` strings, empty `find` arrays, UTF-8 special characters, identical `--input` and `--output` paths
- Write `examples/mapping.json` with genuinely fictional names, not AI-suggested ones

**Definition of done:**
- `python anonymizer/anonymize.py --mapping anonymizer/examples/mapping.json --input anonymizer/examples/note.md --output out/note.anon.md` produces the expected anonymized output
- All acceptance criteria C1–C4 in `ACCEPTANCE.md` pass
- No import of any networking library confirmed by reading `anonymize.py` line 1–20
- Screenshots in `anonymizer/screenshots/` show successful runs on all four file types

---

### AA2 — Real-time Stock Data (Kafka / SSE)

**What AI will help with:**
- Kafka consumer boilerplate using `confluent-kafka` Python library (topic subscription, poll loop, offset commit)
- SSE endpoint scaffolding for the realtime dashboard (Flask or FastAPI `text/event-stream` response)
- Debugging sanitized broker connection errors (e.g., "UNKNOWN_TOPIC_OR_PART")

**What I will do without AI:**
- Configure Kafka broker topics and consumer group IDs specific to this project
- Select the stock symbols and data fields to stream (decide schema myself)
- Verify end-to-end flow manually: producer publishes → topic holds message → consumer reads → dashboard updates
- Confirm the API key is loaded from environment variable only (audit `os.environ` usage)

**Definition of done:**
- Realtime dashboard displays live price updates from the configured Kafka topic in a browser
- History downloader writes complete data to local storage per its README
- `grep -r "API_KEY" kafka-stocks/` returns zero hard-coded credential matches
- Screenshots in `kafka-stocks/screenshots/` show both apps running with real data

---

### Task 03 — Data Storage and Batch Ingestion Pipeline

**What AI will help with:**
- PySpark `DataFrameWriter` Parquet patterns (partition columns, write mode, schema enforcement)
- Drafting `StructType` / `StructField` schema definitions from a sample JSON record
- Writing idempotent overwrite logic with `mode("overwrite")` and partition pruning

**What I will do without AI:**
- Decide the physical storage path, partitioning key, and naming convention for this project
- Validate output Parquet files manually: `spark.read.parquet("data/...").count()` must equal input row count
- Confirm the script runs from a clean directory (no stale checkpoints or partial writes)

**Definition of done:**
- Pipeline reads from source format, writes Parquet partitioned by date with no schema mismatches
- Row count in output equals row count in input (no silent drops confirmed by explicit assertion)
- Script is idempotent: running it twice produces identical output and no duplicate rows

---

### Task 07 — Batch Analysis and Aggregation

**What AI will help with:**
- PySpark aggregation boilerplate: `groupBy`, `agg`, and window function patterns
- Drafting SQL-style analytical query logic for the task report
- Suggesting statistical functions available in `pyspark.sql.functions` for the required metrics

**What I will do without AI:**
- Define the business question and the specific metrics to compute (not delegated to AI)
- Validate aggregated totals against a manually computed sample (spot-check at least 5 rows)
- Write the task report narrative in my own words, not pasted from AI output

**Definition of done:**
- Aggregation script runs on the full dataset without errors or warnings about data skew
- Output report contains expected metrics with values cross-checked against manual calculation
- Task report `documentation/task07_analysis.md` submitted in English with evidence screenshots

---

## 3.8 Disclosure: How This Document Was Produced with AI

This document was produced with significant assistance from **Claude Sonnet 4.6** (Anthropic), accessed via the Claude Code CLI on 2026-05-21. The following describes exactly how AI was used and what was done manually.

**How the AI was prompted:** The complete AA4 specification (`AA4-ai-work-plan.md`, sections 3.1–3.10) was provided together with the course context: ADD project, student ID s34849, repository `s34849_kafka`, and the specific acceptance criteria from `ACCEPTANCE.md` (criteria D1–D9). The AI was asked to produce a complete `documentation/ai-work-plan.md` that satisfies every graded criterion. The repository structure (`anonymizer/`, `kafka-stocks/`, `documentation/`, `consolidation/`) was also described so the AI could include accurate file paths.

**Sections drafted primarily by AI:** Section 3.2 (scope table rows were generated and then reviewed for ADD-specific accuracy), section 3.3 (tools list structure and data-handling notes), section 3.4 (six workflow steps shaped around this project's file structure), section 3.5 (ten prompting rules expanded from the spec's examples), section 3.6 (twelve precautions covering all ten mandatory themes), section 3.7 (four task-specific plans with bullet lists), and section 3.9 (pre-commit checklist).

**What I edited manually after the AI draft:** Section 3.1 was completed with the correct student ID, actual date, and the real repository link. Section 3.7 task names and acceptance criteria references (C1–C4, D1–D9) were cross-checked against the actual `ACCEPTANCE.md` file to ensure they are real and accurate. Section 3.8 (this section) was written entirely by the student after reviewing the draft, because it describes the AI interaction itself and cannot be written by AI without circular reasoning.

**What I rejected from AI suggestions:** The AI initially included a fifth task-specific plan for a visualisation task not yet in scope; this was removed. The AI also proposed adding a Mermaid diagram of the human–AI–review–commit loop under the optional enhancements section; this was omitted to keep the document focused on the mandatory sections and within the word-count ceiling.

**Independent verification:** All acceptance criteria (D1–D9) were manually checked against `ACCEPTANCE.md` after the draft was complete. Word count was verified to exceed 1,200 words. No API keys, passwords, or real personal data appear anywhere in this document.

---

## 3.9 Review Checklist Before Every Commit

Use this checklist before every `git push` to `main` on `s34849_kafka`:

- [ ] I ran the script or application end-to-end on a clean working directory (no leftover `out/` or checkpoint files from a previous run).
- [ ] `git diff HEAD` reviewed in full — no accidentally staged files, no whitespace-only noise, no debug `print` statements left in.
- [ ] No secrets, API keys, `.env` file contents, or passwords appear anywhere in the diff.
- [ ] All file paths referenced in READMEs are verified to exist in the current repository layout.
- [ ] Task report or documentation updated in English to describe the change.
- [ ] Every line of AI-generated code has been read and tested locally before staging.
- [ ] Screenshots in `screenshots/` are updated if CLI output, terminal appearance, or UI changed.
- [ ] Commit message describes the *why*, not just the *what* (e.g., `fix(anonymizer): correct paths after repo restructure`, not `fixed stuff`).
- [ ] `.gitignore` covers all new generated or temporary files introduced by this change (e.g., `out/`, `__pycache__/`, `*.env`).
- [ ] `anonymizer/` CLI still works: `python anonymizer/anonymize.py --mapping anonymizer/examples/mapping.json --input anonymizer/examples/note.md --output out/note.anon.md` runs without error.

---

## 3.10 Revision Log

| Date | Version | Change |
|------|---------|--------|
| 2026-05-21 | 0.1 | Initial draft created with Claude Sonnet 4.6 assistance; all sections 3.1–3.10 present; four task-specific plans included |
| 2026-05-21 | 1.0 | Reviewed and edited manually; task-specific plans verified against ACCEPTANCE.md criteria; visualisation task plan removed as out of scope; section 3.8 (disclosure) written by student; all D1–D9 criteria confirmed present |
