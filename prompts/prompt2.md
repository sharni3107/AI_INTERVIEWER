# AI Transcript — AI Interview Agent Backend (Claude Session)

This document summarizes a multi-turn Claude session used to audit, fix, and
restructure the AI Interview Agent backend for a hackathon submission.
Prompts from the user are marked **User**; Claude's actions and responses
are marked **Claude**.

---

## Turn 1 — Audit real JSON data against the backend implementation

**User** uploaded four files and an audit instruction document:
- `curriculum.json`
- `candidates.json`
- `ai-interview-agent-backend.zip`
- `technical-spec.md`

The instructions asked Claude to:
1. Inspect the real structure of `curriculum.json` and `candidates.json` without inferring fields that aren't present.
2. Audit the backend (services, agents, state, schemas, API layer) for mismatches against the real JSON.
3. Verify the backend meets the interview requirements (personalized planning, curriculum-aware questions, minimum 8 questions, coverage of ≥4 curriculum days, multi-turn conversation, follow-ups, sessionId-based state, answer evaluation, structured feedback, integrity/fraud signals, RAG retrieval, the `POST /api/interview` endpoint).
4. Verify the API contract matched the technical spec.
5. **Modify the existing backend code**, not just report problems.
6. Implement RAG: `curriculum.json → chunks → embeddings → ChromaDB → retriever → agent context`, without hardcoding the 31 days in Python.
7. Ensure candidate personalization used only real candidate fields.
8. Verify `InterviewState` stores everything needed for multi-turn state.
9. Run/update tests after changes.
10. Provide a final report: JSON structure found, backend mismatches, files modified, what changed, files already correct, remaining issues, test results, and exact run/test commands.

### Claude's investigation

- Unzipped the backend and inspected `curriculum.json` — found it was **UTF-16 encoded with a BOM**; converted to UTF-8 to parse it.
- Determined the **real curriculum.json shape**:
  ```
  {"cohort": str, "modules": [{"n", "title", "days": [start, end]}], "days": [{"day", "title", "type", "tools": [], "objectives": []}]}
  ```
  31 days, 8 modules. Day `type` values found: `SETUP, LEARN, BUILD, AI_CORE, OPTIMIZE, SHIP_IT, CAPSTONE`. **No `topic` field and no per-day `module` field** — module membership only derivable from `modules[i].days` (an inclusive day range).
- Determined the **real candidates.json shape**:
  ```
  {"candidates": [{"member": {"id","name","jobRole","yearsExperience","education","status"},
                    "missions": [{"day","title","passed","attempts"} | {"day","title","skipped": true}],
                    "signals": {"commitDays","missionsCompleted","missionsFirstTry"}}]}
  ```
  20 candidates. **No `score`, `project`, `strong_areas`, or `weak_areas` fields anywhere.**
- Compared this against the backend's own bundled sample data (`data/curriculum.json`, `data/sample_candidate.json`) and found the backend had been built against a **fabricated schema** using `module`/`topic` per day and `completed_missions`/`skipped_topics`/`learning_signals`/`project` for candidates — none of which exist in the real files.
- Found **no RAG/ChromaDB pipeline existed at all**, despite a code comment in `curriculum_service.py` claiming "no RAG needed."
- Reviewed every backend file (`curriculum_service.py`, `candidate_service.py`, `planner.py`, `interviewer.py`, `evaluator.py`, `feedback.py`, `orchestrator.py`, `interview_state.py`, `state_machine.py`, `state_manager.py`, `interview.py` schema, `interviews.py` API route, `llm.py`, `integrity.py`, `main.py`, `config.py`, tests, `demo.py`) to determine what was correct vs. broken.

### Fixes implemented

- Replaced `backend/data/curriculum.json`, `candidates.json`, `techspec.md`, and `sample_candidate.json` with the real uploaded data (sample candidate = `CAND-001`, Sarah Johnson: 8 passed missions across 8 distinct days, 1 skipped day).
- Rewrote **`curriculum_service.py`** to use the real `title`/`type` fields and to derive a day's module via the `modules[].days` inclusive range.
- Built a real RAG pipeline:
  - **`app/rag/ingest.py`** — chunks each curriculum day into one text chunk (title, type, tools, objectives, derived module).
  - A `HashingEmbeddingFunction` — a small, dependency-free, offline embedding function (hashed bag-of-words → 256-dim vector, L2-normalized), used **instead of** ChromaDB's default ONNX/HuggingFace embedding function because the sandbox had no outbound network access to a model-weights host.
  - **`app/rag/retriever.py`** — `CurriculumRetriever.retrieve(query, n_results)` for semantic search, plus `retrieve_days_for_topics()` used by the planner to widen weak-area coverage.
  - Verified via a standalone script that semantic search correctly surfaced relevant days (e.g. a query about "vector databases and embeddings" returned the Embeddings & Vector Search module days).
- Rewrote **`candidate_service.py`**'s `normalize_candidate()` to match the real `member`/`missions`/`signals` schema, deriving `passed_days`, `failed_days`, `skipped_days`, `attempted_days`, and `struggled_days` (missions needing ≥3 attempts, or attempted-but-not-passed — the only "difficulty" signal that actually exists in the data).
- Rewrote **`planner.py`** to personalize from the real candidate fields, prioritizing struggled days first and falling back to RAG-widened day selection when there weren't enough struggled days.
- Updated **`interviewer.py`** and **`evaluator.py`** to use `day_info.get("title")` instead of the fabricated `"topic"` field, and real candidate background fields (`job_role`, `years_experience`, `education`) instead of the fabricated `"project"` field.
- Added `integrity_flags` storage to **`InterviewState`** and wired **`orchestrator.py`** to record integrity check results (empty/too-short/echoed answers) onto state instead of just logging them.
- Updated **`feedback.py`** to fold integrity signals into the final feedback's `gaps` when present.
- Added `chromadb` to `requirements.txt`.
- Rewrote **`tests/conftest.py`** with a real candidate fixture (`SAMPLE_CANDIDATE`, matching `CAND-001`) and a scripted mock LLM responder for deterministic multi-turn tests.
- Added new test files: `test_curriculum_service.py`, `test_candidate_service.py`, `test_rag.py`, `test_planner.py`; extended `test_session.py` and `test_api.py` with coverage-floor and integrity-flag tests.
- Rewrote **`demo.py`** to be schema-agnostic (reads eligible curriculum days out of the real planner prompt via regex, rather than hardcoding fake days/topics) and to run against the real `sample_candidate.json`.

### Debugging notes

- Initial `demo.py` regex only matched the planner's multi-day prompt format (`Day N [...`), so the interviewer's single-day prompt (`Day N - Title`) fell through to a hardcoded fallback of day 1, causing repeated questions on the same day. Fixed by adding a second regex pattern and separating "pick first eligible day" (planner call) from "extract the day the plan already chose" (interviewer call).
- Fixed a ChromaDB `EmbeddingFunction` deprecation warning by implementing `get_config()`/`build_from_config()` and making `name()` a `@staticmethod` as chromadb's protocol expects.

### Result

- **48/48 tests passed.**
- `demo.py` completed an 8-question interview across 8 real curriculum days with valid structured feedback.
- A live `curl` against a running `uvicorn` server confirmed the full flow worked end-to-end over real HTTP.
- Delivered: `ai-interview-agent-backend-fixed.zip`.
- Final report included: JSON structure found, mismatches found, files modified with descriptions of each change, files that were already correct and needed no changes, remaining issues (none blocking), test results, and exact commands to run the backend and test the endpoint.

---

## Turn 2 — File-by-file explanation

**User:** *"okay now explain code file by code file and why we are doing it so that i will be able to understand and do modifications if needed"*

**Claude** provided a structured walkthrough of the backend following the request flow (`config → data loading → RAG → candidate normalization → state → agents → orchestrator → API layer → tests`), explaining for each file:
- What it does
- Why it's structured that way
- Where to make changes if the person wants to modify behavior

Files covered: `core/config.py`, `services/curriculum_service.py`, `rag/ingest.py` + `rag/retriever.py`, `services/candidate_service.py`, `state/interview_state.py`, `state/state_manager.py`, `state/state_machine.py`, `agents/llm.py`, `agents/planner.py`, `agents/interviewer.py`, `agents/evaluator.py`, `agents/integrity.py`, `agents/feedback.py`, `agents/orchestrator.py`, `services/interview_service.py`, `api/interviews.py` + `schemas/interview.py`, `app/main.py`, `tests/conftest.py`, `tests/test_*.py`, `demo.py` — ending with guidance on dependency order for making safe changes.

---

## Turn 3 — Restructure to a clean MVP for hackathon submission

**User** gave a new, stricter set of requirements, explicitly warning against over-engineering:

> "Review the current backend structure against the AI Interview Agent hackathon requirements. IMPORTANT: Do not blindly create unnecessary enterprise architecture."

The 16 stated requirements:
1. `POST /api/interview`
2. sessionId-based interview state
3. Candidate JSON input
4. Curriculum JSON usage
5. Minimum 8 questions
6. Questions covering ≥4 curriculum days
7. Adaptive follow-up questions
8. Multi-turn conversation context
9. Structured final feedback (`summary`, `strengths[]`, `gaps[]`, `next[]`)
10. OpenRouter as the LLM provider
11. GPT-4o Mini through OpenRouter
12. No authentication
13. No persistent user accounts
14. No long-term conversation history
15. No voice/video
16. No database requirement

The user provided a **specific recommended folder structure** (`agents/`, `api/`, `core/`, `rag/{embeddings.py, ingest.py, retriever.py}`, `schemas/{candidate,interview,evaluation,report}.py`, `services/{candidate,curriculum,interview,evaluation,report}_service.py`, `state/`, `utils/{logger.py, candidate_normalizer.py}`, `main.py`, `data/`, `tests/{test_interview.py, test_evaluation.py}`, `requirements.txt`, `.env`) and explicitly said:

> "Do NOT add: database/, models/, authentication, admin APIs, analytics APIs, separate candidate/course APIs, persistent user accounts, unnecessary planner/integrity agents."

And specified the exact required flow:
```
POST /api/interview → candidate normalization → candidate + curriculum analysis
→ create session state → generate first question → candidate responds
→ evaluate answer → generate adaptive follow-up → repeat until ≥8 questions
→ ensure ≥4 curriculum days covered → generate final feedback
→ return summary/strengths/gaps/next
```

> "Use OpenRouter with GPT-4o Mini. Do not use OpenAI API directly. Do not use Anthropic API directly."

The user also required Claude to inspect first, compare against the structure, reuse useful files, delete unnecessary files only if clearly unused, avoid duplicating functionality, and confirm the implementation actually works end-to-end.

### Claude's review

Identified that the previous (Turn 1) backend, while functionally correct, was **over-built for this scope**:
- A separate `planner.py` LLM agent existed just to decide "next day / follow-up / complete" — an extra LLM call for a decision that's actually deterministic given candidate + curriculum data.
- A separate `integrity.py` agent existed — not in the 16 stated requirements.
- The LLM provider was Anthropic-only and needed to become OpenRouter + GPT-4o Mini via raw HTTP (no SDK).
- Several files specified in the recommended structure didn't exist yet: `rag/embeddings.py` (embedding function was inline in `ingest.py`), `schemas/candidate.py`/`evaluation.py`/`report.py` (dataclasses lived in `state/interview_state.py`), `utils/candidate_normalizer.py` (normalization logic lived in `services/candidate_service.py`), `services/evaluation_service.py`, `services/report_service.py`.

### Restructuring implemented

- **`core/config.py`** — replaced Anthropic settings with `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, default model `openai/gpt-4o-mini`; added optional `.env` loading via `python-dotenv`.
- **`core/llm_client.py`** (new location, moved out of `agents/`) — `OpenRouterLLMClient` calling OpenRouter's `/chat/completions` endpoint directly via `httpx` (no `openai`/`anthropic` SDK), plus `MockLLMClient` for offline tests/dev. Deleted the old `agents/llm.py`.
- **`rag/embeddings.py`** (new) — the offline hashing embedding function, split out of `ingest.py` to match the required structure.
- **`utils/candidate_normalizer.py`** (new) — the pure `normalize_candidate()` function moved out of `services/candidate_service.py`.
- **`services/candidate_service.py`** — rewritten as a thin wrapper re-exporting the normalizer, plus a new `get_prioritized_days()` function: the deterministic day-selection logic (struggled-days-first, RAG-widened) that **replaces the removed planner agent** without needing an LLM call.
- **`schemas/evaluation.py`, `schemas/report.py`, `schemas/candidate.py`** (new) — dataclasses/TypedDict moved out of `interview_state.py` into dedicated schema files. `schemas/interview.py` extended to also hold `QuestionRecord`.
- **`state/interview_state.py`** — rewired to import from `schemas/`; **`integrity_flags` field removed** entirely (no integrity agent anymore).
- **`state/state_machine.py`** — simplified the old `AdaptiveDecision` enum into a smaller `TurnDecision` enum (`FOLLOW_UP` / `NEW_TOPIC` / `COMPLETE`), with `can_force_complete()` and `meets_completion_floor()` guardrails retained.
- **`agents/interviewer.py`** — decoupled from the removed `InterviewPlan` dataclass; now takes explicit `(curriculum_day, difficulty, is_follow_up, objective)` parameters.
- **`agents/evaluator.py`**, **`agents/feedback.py`** — import paths updated; integrity references removed from feedback generation.
- **Deleted** `agents/planner.py` and `agents/integrity.py` entirely, per the explicit instruction.
- **`services/evaluation_service.py`** (new) — thin wrapper: calls the evaluator agent, records the result onto session state.
- **`services/report_service.py`** (new) — thin wrapper: calls the feedback agent, marks the session completed.
- **`agents/orchestrator.py`** — rewritten as the deterministic "brain": `_decide_next_step()` decides `FOLLOW_UP` / `NEW_TOPIC` / `COMPLETE` in plain Python (no LLM call), then delegates question generation, evaluation, and feedback to the three real LLM agents.
- **`api/interviews.py`**, **`app/main.py`** — import paths and docstrings updated for OpenRouter.
- **`requirements.txt`** — removed `anthropic`, added `python-dotenv`.

This turn was interrupted mid-way (tool-call limit reached) with tests, `demo.py`, and the README still needing updates — Claude summarized progress and what remained before stopping.

---

## Turn 4 — Continue and deliver

**User:** *"Continue"*

**Claude** found that the old test files still referenced the removed modules (`agents.llm`, `agents.planner`, `agents.integrity`, `integrity_flags`, `AdaptiveDecision`) and would fail to import. Consolidated the test suite down to match the recommended structure:

- Deleted the old test files (`test_planner.py`, `test_rag.py`, `test_session.py`, `test_api.py`, `test_interview_flow.py`, `test_candidate_service.py`, `test_curriculum_service.py`, old `conftest.py`).
- Rewrote **`tests/conftest.py`** with the real `SAMPLE_CANDIDATE` fixture and a scripted mock LLM responder matching the new (planner-free) orchestrator's two remaining LLM call shapes (question generation, answer evaluation) plus the final feedback call.
- Created **`tests/test_interview.py`** — candidate normalization, curriculum service, RAG retrieval, session state, and the full `POST /api/interview` API lifecycle.
- Created **`tests/test_evaluation.py`** — evaluator agent, `EvaluationService`, `FeedbackAgent`/`ReportService`, and `candidate_service.get_prioritized_days()` personalization.

### Debugging steps

- While writing the scripted test responder, found and fixed a real bug in **`interviewer.py`**: `raw.get("curriculum_day", curriculum_day)` only falls back to the default when the key is *absent*, not when its value is explicit `null` — so if the LLM (or a test mock) returned `"curriculum_day": null`, it would silently override the orchestrator's chosen day with `None`, breaking curriculum-day coverage tracking. Fixed by changing to `raw.get("curriculum_day") or curriculum_day` (and the same pattern for `difficulty`).
- Ran the new test suite: **29/30 passed, 1 failure** — `test_missing_candidate_on_start_is_rejected` expected `400` but got `404`. Investigated `api/interviews.py`'s routing and found that when `candidate` is absent, the request is always routed to "continue" mode (`process_message`), so a brand-new, never-started session correctly raises `SessionNotFoundError` → `404`, not `MissingCandidateError` → `400` (which is effectively dead code given the current routing). Corrected the test's expectation to match this real, reasonable behavior rather than changing the routing logic, and added a new test (`test_empty_candidate_object_on_start_is_rejected`) to properly cover the `400` case (starting a session with an empty `candidate: {}` payload).
- Re-ran the suite: **31/31 passed.**

### Remaining cleanup

- Rewrote **`demo.py`** for the new orchestrator (removed the old regex-based day-extraction hack, since the orchestrator now picks the day deterministically before calling the interviewer). Verified it completes an 8-question interview across 8 distinct real curriculum days with valid structured feedback.
- Added **`.env`** (defaults to `LLM_PROVIDER=mock`) and **`.env.example`** (defaults to `LLM_PROVIDER=openrouter`) with all config variables documented.
- Rewrote **`README.md`** to reflect the new structure, OpenRouter/GPT-4o Mini usage, the full request flow, and an explicit "Why no separate planner or integrity agent" section explaining the design decision.
- Grepped the full repo for stale references to removed modules — none found outside of an intentional test asserting `integrity_flags` no longer exists on `InterviewState`.
- Confirmed the final `app/` directory tree matches the user's recommended structure exactly.
- Ran the full test suite fresh (after clearing caches): **31/31 passed.**
- Ran a live smoke test: started `uvicorn` with `LLM_PROVIDER=mock`, hit `/health`, then `POST /api/interview` twice via `curl` — confirmed the welcome message, first question, and an **adaptive follow-up question** (triggered by a short/weak answer) all worked correctly over real HTTP.
- Verified the `OpenRouterLLMClient` raises a clear `LLMError` ("OPENROUTER_API_KEY is not set...") rather than failing silently or falling back, when `LLM_PROVIDER=openrouter` is set without a key.
- Cleaned all `__pycache__`, `.pytest_cache`, and ChromaDB temp directories before packaging.
- Zipped and delivered the final backend as **`ai-interview-agent-backend-mvp.zip`**, confirming via `unzip -l` that `.env`, `.env.example`, and `data/sample_candidate.json` were all included.

### Final structure delivered

```
app/
├── agents/{interviewer,evaluator,feedback,orchestrator}.py
├── api/interviews.py
├── core/{config,llm_client}.py
├── rag/{embeddings,ingest,retriever}.py
├── schemas/{candidate,interview,evaluation,report}.py
├── services/{candidate,curriculum,interview,evaluation,report}_service.py
├── state/{interview_state,state_manager,state_machine}.py
├── utils/{logger,candidate_normalizer}.py
└── main.py
data/{curriculum.json, candidates.json, sample_candidate.json, techspec.md}
tests/{test_interview.py, test_evaluation.py}
requirements.txt
.env / .env.example
```

### Key design decisions explained by Claude

- No separate "planner" agent: curriculum-day selection and follow-up-vs-new-topic decisions are deterministic Python (`services/candidate_service.get_prioritized_days()` + `agents/orchestrator._decide_next_step()`), backed by guardrails in `state/state_machine.py` (hard floor: ≥8 questions and ≥4 days before `COMPLETE` is allowed; hard ceiling: ≤16 questions regardless). This keeps the pipeline to exactly 2 LLM calls per turn (question + evaluation) plus 1 at the end (feedback).
- No separate integrity agent: not a stated requirement; the evaluator's `follow_up_needed`/`suggested_follow_up_area` output already naturally surfaces thin answers by prompting a follow-up.
- Adaptive follow-up: after each answer, if the evaluator flags `follow_up_needed` and the score is below 7, the orchestrator asks one follow-up on the same topic — never chaining two follow-ups back to back — then moves to a new curriculum day. Difficulty nudges up after a strong answer (score ≥8) and down after a weak one (score ≤4).
- RAG's role is narrow and functional, not decorative: it only kicks in to widen the eligible-day pool when a candidate has fewer than 2 "struggled" days, using semantic similarity to their struggled mission titles.

### Result

- **31/31 tests passed.**
- `demo.py` and a live `curl` smoke test both confirmed the full flow works end-to-end, including adaptive follow-up questions.
- Delivered: **`ai-interview-agent-backend-mvp.zip`**.

---

## Files delivered across the session

| File | Turn | Description |
|---|---|---|
| `ai-interview-agent-backend-fixed.zip` | 1 | First-pass audit/fix: real data wired in, RAG added, schema mismatches corrected, integrity/planner agents present |
| `ai-interview-agent-backend-mvp.zip` | 4 | Final clean MVP restructure: OpenRouter/GPT-4o Mini, planner/integrity agents removed, folder structure matches hackathon spec exactly |


