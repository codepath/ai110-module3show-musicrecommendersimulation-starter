# AI Interactions Log

This file documents the **stretch features** built on top of the required chat
interface: an **agentic workflow** and a **RAG enhancement**. The full,
reproducible reasoning traces live in [`logs/agent_traces.md`](logs/agent_traces.md)
(regenerate with `python scripts/generate_traces.py`).

---

## Agentic Workflow — multi-step reasoning with tool-calls

**What it does.** Every chat message runs through an explicit decision chain in
[`src/agent.py`](src/agent.py) instead of a single fixed path:

1. **PLAN** — read the message for question-vs-request cues and pre-parse taste terms; form a hypothesis about which tool to use.
2. **ACT** — call a tool: the **knowledge retriever** (`src/knowledge_base.py`) or the **recommender** (`src/recommender.py`).
3. **CHECK** — inspect the tool's result. If the hypothesis was wrong — a "question" that grounds nothing, or a "request" with no parseable taste — **re-route** and call the other tool (a reflection step).
4. **RESPOND** — return the grounded answer.

The two tools are the project's own functions, so the whole loop is deterministic
and offline. Each step is recorded and shown in the app's "Agent steps" panel.

**Example trace — the re-route (reflection) path.** The message is *phrased* as a
question, so the agent tries the knowledge tool first; it grounds nothing, but a
taste term was parsed, so the agent changes plan and calls the recommender:

```
User: can you play something euphoric?
Intent chosen: recommend

1. [PLAN] question-like=True; parsed taste={'mood': 'euphoric'} → try the knowledge tool first
2. [ACT] called knowledge retriever → grounded=False, score=0.00, top_source=None
3. [CHECK] not grounded, but taste terms were parsed → RE-ROUTE to recommend
4. [ACT] called recommender → 5 picks
5. [RESPOND] returned recommendations
```

**How it was verified.** [`tests/test_agent.py`](tests/test_agent.py) asserts each
routing path, including that the re-route emits a `CHECK … RE-ROUTE` step and that
a trace is always produced. See `logs/agent_traces.md` for one trace per path.

---

## RAG Enhancement — retrieval over a second data source

**What it does.** The original system had one data source (the song catalog) and
one kind of retrieval (content-based scoring → songs). The enhancement adds a
**second data source** — fact documents in [`data/knowledge/`](data/knowledge/)
(a genre glossary and a "how it works" FAQ) — and a **keyword retriever** in
[`src/knowledge_base.py`](src/knowledge_base.py) that answers *questions about*
music grounded in those docs, with citations and a relevance threshold that makes
it say "I don't have that" instead of guessing.

**Before → after** (message: *"what is lofi?"*):

- **Before** (recommender only): the word "lofi" is parsed as a genre and the
  system returns a *list of lofi songs* — it never answers the question.
- **After** (agent routes to the retriever): the system returns a grounded
  definition from `genres.md`:

  ```
  Intent chosen: knowledge
  [ACT] called knowledge retriever → grounded=True, score=1.00, top_source=genres.md
  Reply: **Lofi** — Lofi (short for "low-fidelity") is relaxed, downtempo music
  built around mellow beats, soft instrumentation, and a warm, slightly hazy sound...
  ```

**How it was verified.** [`tests/test_knowledge_base.py`](tests/test_knowledge_base.py)
covers chunking, heading-weighted ranking, the grounding threshold (an unrelated
question is *not* grounded), and the honest fallback answer.
