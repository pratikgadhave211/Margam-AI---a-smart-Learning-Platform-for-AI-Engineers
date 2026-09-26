# Margam AI — Learning Platform for AI Engineers
*(Working name: Margam AI — from Sanskrit/Tamil "Margam," a structured learning progression from simple to complex)*

## 1. Vision & Positioning

Build a learning platform for AI engineers that becomes what LeetCode is for DSA — but the core mechanic isn't algorithmic puzzles, it's **design judgment**: making the right architectural calls when building RAG pipelines and AI agents, and knowing how to debug and optimize them.

**The flagship feature is practical questions, not MCQs.** MCQs and learning paths exist, but they are secondary/retention features layered on top of a working practical-questions core.

The core loop, modeled on why LeetCode worked:
> Scenario → your design/answer or code → structured feedback → compare to a strong reference solution → retry

## 2. Content Structure

### Learning paths (sequential tracks)
- ML Fundamentals
- DL Fundamentals
- GenAI / LLM Foundations
- RAG Track
- Agentic AI Track
- Interview Prep (timed, mixes everything, company/role-focused)

### Two problem sections per path
1. **MCQ** — conceptual, auto-graded, secondary content
2. **Practical** — scenario-based build/optimize/debug/code questions — the flagship feature

### Practical question types
- **Build** — design a RAG pipeline or agent architecture for a given scenario
- **Optimize** — improve a working-but-flawed system (accuracy, latency, cost) — should use real measurable metrics, not just opinion
- **Debug** — given a broken pipeline/agent trace, find and fix the root cause
- **Code** — LeetCode-style: implement specific functions/methods against premade infrastructure, graded by weighted test cases

## 3. Question Design Discipline

Every question must be built like a well-designed LeetCode problem: it teaches exactly **one** concept, and the scenario is engineered so a naive/wrong approach visibly fails — the person shouldn't be able to stumble past the lesson by accident.

**Authoring checklist for every question:**
1. What's the one concept? (pick exactly one concept tag — never mix several into one question)
2. What's the naive/wrong approach someone would try?
3. What in the scenario makes the naive approach *visibly* fail? (a concrete data characteristic, not "trust me")
4. What's the one insight that fixes it? (this becomes the rubric's core hit/miss element)

### Concept taxonomy (RAG)
| Concept tag | The "aha" | Scenario trap |
|---|---|---|
| `chunking-strategy` | Fixed-size chunking breaks structured docs | Contracts/code/tables — fixed-size visibly fails |
| `retrieval-type` | Dense embeddings miss exact-match needs | Scenario with IDs/codes/citations — dense-only fails |
| `re-ranking` | Top-k cosine similarity isn't precision | Many near-duplicate chunks crowd out the best one |
| `metadata-filtering` | Semantic search can't enforce hard constraints | Date/category constraint baked into the question |
| `chunk-overlap` | Losing boundary context breaks multi-step facts | Answer spans a chunk boundary |
| `prompt-caching` | Re-sending static content on every call wastes cost/latency | Growing conversation history sent raw alongside static system prompt/tools |
| `context-window-management` | Naive oldest-first trimming drops critical facts | A hard constraint stated early gets silently trimmed |

### Concept taxonomy (Agentic AI)
| Concept tag | The "aha" | Scenario trap |
|---|---|---|
| `agent-topology` | One agent overloaded with unrelated tools degrades | Mixed unrelated tool domains confuse tool selection |
| `orchestration-pattern` | Peer agents without a coordinator can't enforce order | Sequential dependency needed, swarm races |
| `tool-design` | Vague/overlapping tool descriptions cause wrong calls | Two similar-sounding tools, ambiguous descriptions |
| `agent-memory` | Session memory doesn't survive across sessions | Multi-day task loses continuity |
| `agent-guardrails` | Missing exit condition causes infinite loops | Retry loop with no termination check |

Both taxonomies are extensible — add new concept tags as new question ideas surface, following the same authoring checklist.

## 4. Evaluation Techniques (per question type, not one-size-fits-all)

| Question type | Evaluation technique |
|---|---|
| Design/Build | Layer 1: deterministic config-match scoring. Layer 2: LLM-as-judge grading against a rubric (list of must-hit reasoning points, not a single model answer) |
| Debug | Root-cause localization — user identifies the specific faulty step/line, graded against the one known bug, not a menu of designs |
| Optimize | Metric-based grading — run before/after against a small golden eval set, score = the real measured delta on a real metric |
| Code | Sandboxed unit tests — weighted, prioritized test cases (see Section 5) |
| Agent trace/orchestration | Trace validator — rule-based invariant checking (e.g. "tool X must not be called before tool Y"), not exact-sequence matching, since multiple valid trajectories can be correct |
| MCQ | Trivial deterministic auto-grade |

### Real, industry-standard metrics to use (not invented rubrics)

**RAG retrieval-side:** Precision@k, Recall@k, MRR, NDCG, Hit Rate

**RAG generation-side (RAGAS-style):** Faithfulness, Answer Relevancy, Context Precision, Context Recall — RAGAS (open-source, LangChain-integrated) can compute these automatically given (question, retrieved contexts, generated answer, ground truth)

**Agent-side:** Task success rate, Tool-call precision/recall, Trajectory match (vs. a reference "good" trajectory), Step efficiency, Cost/latency

**Where these plug in:**
- Optimize questions: precompute baseline metric on a golden set → user submits fix → recompute → score = the delta (e.g. "Faithfulness improved from 0.61 → 0.89")
- Design questions: precompute the metric each design choice *would* produce once, offline, and show it as the ground truth instead of an opaque "correct answer"
- Debug questions: a low Faithfulness/Context Recall score can be the symptom shown to the user before they diagnose the cause

## 5. Coding-Question Format (LeetCode-style, the concrete build target)

- User selects a question: difficulty (easy/medium/hard), sees description, hints (progressively revealable), topic tags, learning resources, input/output examples
- Editor presents a starter class (e.g. `RAG`) with **premade** components (vector store, documents already loaded) and **stub methods** for the parts the user implements (e.g. `chunk()`, `embed()`, `retrieve()`)
- **10 test cases per question**, each with:
  - Priority: high / medium / low
  - Target function
  - Input, expected output
  - Comparison method — **critical nuance:** we compare *outputs*, never source code, and the equality function differs by output type:
    - `exact` — deterministic outputs (e.g. `chunk()` given fixed doc + params)
    - `tolerance` — floating point outputs (e.g. `embed()` — compare with `numpy.allclose` or cosine similarity ≈ 1.0, never raw float equality)
    - `property_check` — structural properties (e.g. correct vector dimension, normalization)
    - `precision_at_k` — set/ranking-based outputs (e.g. `retrieve()` when multiple valid answers exist)
  - `concept_hint_tag` — links a failing test to a specific hint, so feedback is specific, not generic
- Test cases run **concurrently** within one sandboxed instance (shared premade state, no side effects between calls)
- **Scoring:** `score = Σ(passed_i × weight[priority_i]) / Σ(weight[priority_i]) × 100`, weights e.g. `{high: 3, medium: 2, low: 1}`
- **Threshold** determines success/fail
- **Feedback:** success → greeting message. Failure → group failed tests by `concept_hint_tag`, surface the hint for the highest-weighted failing group, show a summary (not a raw per-test dump)

## 6. End-to-End Architecture

**Flow: question click → submission → pass/fail**

1. **Client** — question catalogue, code editor, submit button; JWT auth on every request
2. **API layer (FastAPI)** — `GET /scenarios`, `GET /scenarios/{id}` (no answers/test cases exposed), `POST /submissions` (creates `pending` record, enqueues job, returns immediately), `GET /submissions/{id}` (polling), rate limiting per user
3. **Data layer (PostgreSQL + SQLAlchemy/Alembic)**
   - Admin-authored, read-mostly: `scenarios`, `test_cases`, `rubrics`, `golden_eval_sets`
   - User-generated: `submissions`, `submission_results` (one row per test case), `users`
4. **Artifact storage** — documents in object storage; vector store precomputed once per scenario at authoring time, persisted to disk (never rebuilt per submission)
5. **Caching (Redis)** — caches loaded vector store/documents per scenario; doubles as the task queue broker
6. **Queue & worker pool (Redis + Celery/ARQ)** — horizontally scalable workers, one job per submission
7. **Sandboxed execution** — Docker container (or nsjail/gVisor), CPU/memory/time limits, **no network access**; loads cached vector store/docs read-only; injects user code into the premade class, instantiates it
8. **Test execution engine** — runs all test cases concurrently inside the sandbox, applies the correct comparator per test, captures pass/fail + actual output + timing
9. **Scoring engine** — weighted score formula above; for design-type questions, the LLM-judge rubric call runs as a **separate process from the sandbox** (needs network access; the sandbox must not have any)
10. **Feedback generation** — pass/fail message as described in Section 5
11. **Persistence & notification** — write `submission_results` + update `submissions` (score, status, feedback); client gets the result via polling `GET /submissions/{id}` (MVP) or WebSocket push (later)
12. **Observability** — log execution time, pass rate, sandbox resource usage; alert on repeated sandbox crashes/timeouts per scenario (usually a miscalibrated test case, not bad user code)

## 7. Tech Stack (matches existing skills)
- **Backend:** FastAPI, async endpoints/streaming
- **DB:** PostgreSQL + SQLAlchemy/Alembic
- **Agents/grading:** LangGraph (rubric grader, study-planner agent)
- **Queue:** Redis + Celery/ARQ
- **Sandbox:** Docker (or nsjail/gVisor for tighter isolation)
- **Vector store:** for premade scenario retrieval corpora, and for rubric/reference-answer search
- **Auth:** existing auth/security work
- **Deployment:** Docker, CI

## 8. AI Assistant Features (post-MVP)

Two distinct agent roles, inspired by Deep-ML's "Zero" assistant:
1. **Solving-time agent** — reads the scenario + user's current answer/code, gives progressive hints (gated behind explicit reveal, never spoils unprompted), doubles as the LLM-judge grader (same context, built once, reused for both)
2. **Study-planner agent** — recommends problems/paths based on stated goals, builds a clickable playlist from the problem catalogue

## 9. Build Order (practical-questions-first, backend-first)

1. **Prove the core loop on one question type first.** Seed one design-type question (e.g. chunking strategy), build the grading graph for Layer 1 + Layer 2 only, wire one API endpoint, hit it from a bare-bones frontend page.
2. Expand scenario coverage — add agent-design, debug, optimize scenarios in the same layered format.
3. Build the coding-question format end-to-end (Section 5/6) for one scenario — sandbox, test harness, scoring, feedback.
4. Add the solving-time agent (hints + grading).
5. Layer in MCQs, learning paths, contests, leaderboard — retention/breadth features, secondary.
6. Add the study-planner agent.
7. Expand code-execution to more scenarios; add real metric harnesses (RAGAS, trajectory match) for optimize/debug questions at scale.

**Do not build all question types or all infra pieces before proving the first end-to-end loop works.**

## 10. Open / Future Ideas Log
- Context window management as its own question sub-category (naive trimming trap, prompt-caching/static-dynamic separation, "context rot" detection)
- More agentic scenario variants: multi-agent context sharing, summarization drift over repeated compressions
- Contests, leaderboard, playlists, discuss forum (secondary features, post-MVP)
