"""
Agentic workflow for the MoodMatch chat (stretch feature).

Instead of a single hard-coded path, each user message runs through an explicit
multi-step reasoning chain with tool-calls and a decision point that can change
its own plan:

    1. PLAN    -- read the message for question vs. request cues; form a hypothesis
    2. ACT     -- call a tool: the knowledge retriever OR the recommender
    3. CHECK   -- inspect the tool's result; if the hypothesis was wrong
                  (e.g. a "question" nothing grounds, or a "request" with no
                  parseable taste), RE-ROUTE and call the other tool
    4. RESPOND -- format the final grounded answer

Every step is recorded on the result's `steps` list, so the reasoning trace can
be shown in the UI and saved to ai_interactions.md. The whole thing is
deterministic and offline -- the "tools" are the project's own functions.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional

# Dual-import guard so this runs under `streamlit run`, `-m src.agent`, or direct.
try:
    from src.recommender import load_songs, recommend_songs, score_ceiling
    from src.query_parser import build_vocab, parse_query
    from src.knowledge_base import load_knowledge, answer_question, retrieve, Retrieval
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, score_ceiling
    from query_parser import build_vocab, parse_query
    from knowledge_base import load_knowledge, answer_question, retrieve, Retrieval

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# Cues that a message is a question about music/the system rather than a request
# for songs. The retriever's grounding is the real arbiter; this only sets the
# initial hypothesis the CHECK step then confirms or overturns.
QUESTION_STARTERS = (
    "what", "what's", "whats", "how", "why", "who", "when", "where", "which",
    "does", "do", "is", "are", "can", "could", "explain", "tell", "define",
)
QUESTION_PHRASES = ("difference between", "what is", "what are", "how does", "how do")

EMPTY_HINT = (
    "I couldn't pick up a genre, mood, or vibe from that, and it isn't a question "
    "I have notes on. Try a request like **\"chill lofi for studying\"** or a "
    "question like **\"what is lofi?\"**."
)


@dataclass
class AgentStep:
    """One step in the reasoning trace."""
    name: str      # PLAN | ACT | CHECK | RESPOND
    detail: str


@dataclass
class AgentResult:
    """The agent's answer plus everything needed to display or log its reasoning."""
    reply: str
    intent: str                                  # knowledge | recommend | fallback
    steps: List[AgentStep] = field(default_factory=list)
    prefs: Optional[dict] = None
    recommendations: Optional[list] = None
    retrieval: Optional[Retrieval] = None


def _looks_like_question(text: str) -> bool:
    """Heuristic: does this read like a knowledge question rather than a taste request?"""
    t = (text or "").strip().lower()
    if not t:
        return False
    if "?" in t:
        return True
    if any(t.startswith(starter + " ") or t == starter for starter in QUESTION_STARTERS):
        return True
    return any(phrase in t for phrase in QUESTION_PHRASES)


class Agent:
    """Holds the loaded data/tools and runs the plan-act-check-respond chain."""

    def __init__(self, songs=None, chunks=None):
        self.songs = songs if songs is not None else load_songs(DATA_PATH)
        self.chunks = chunks if chunks is not None else load_knowledge()
        self.genre_phrases, self.mood_phrases = build_vocab(self.songs)

    # --- tools -------------------------------------------------------------
    def _tool_recommend(self, prefs: dict, k: int = 5):
        """Recommendation tool: rank the catalog and format a reply."""
        ceiling = score_ceiling(prefs, self.songs)
        recs = recommend_songs(prefs, self.songs, k=k)
        lines = ["Here are some picks for you:\n"]
        for i, (song, score, explanation) in enumerate(recs, start=1):
            normalized = 10.0 * score / ceiling if ceiling else 0.0
            lines.append(
                f"{i}. **{song['title']}** — {song['artist']} "
                f"[{song['genre']}/{song['mood']}]  ({normalized:.1f}/10)\n"
                f"   _{explanation}_"
            )
        return "\n".join(lines), recs

    def _tool_knowledge(self, text: str):
        """Knowledge tool: retrieve a grounded answer from the fact docs."""
        return answer_question(text, self.chunks)

    # --- the chain ---------------------------------------------------------
    def run(self, text: str) -> AgentResult:
        steps: List[AgentStep] = []
        prefs = parse_query(text, self.genre_phrases, self.mood_phrases)
        question_like = _looks_like_question(text)
        plan = "knowledge" if question_like else "recommend"
        steps.append(AgentStep(
            "PLAN",
            f"question-like={question_like}; parsed taste={prefs or '{}'} "
            f"→ try the {plan} tool first",
        ))

        if plan == "knowledge":
            answer, retrieval = self._tool_knowledge(text)
            src = retrieval.hits[0].source if retrieval.hits else None
            steps.append(AgentStep(
                "ACT", f"called knowledge retriever → grounded={retrieval.grounded}, "
                       f"score={retrieval.score:.2f}, top_source={src}"))
            if retrieval.grounded:
                steps.append(AgentStep("CHECK", "retrieval is grounded → answer from docs"))
                steps.append(AgentStep("RESPOND", "returned document-grounded answer"))
                return AgentResult(answer, "knowledge", steps, prefs=prefs, retrieval=retrieval)
            # Reflection: the question didn't ground. Is it actually a taste request?
            if prefs:
                steps.append(AgentStep(
                    "CHECK", "not grounded, but taste terms were parsed → RE-ROUTE to recommend"))
                reply, recs = self._tool_recommend(prefs)
                steps.append(AgentStep("ACT", f"called recommender → {len(recs)} picks"))
                steps.append(AgentStep("RESPOND", "returned recommendations"))
                return AgentResult(reply, "recommend", steps, prefs=prefs, recommendations=recs)
            steps.append(AgentStep(
                "CHECK", "not grounded and no taste terms → answer honestly that it's unknown"))
            steps.append(AgentStep("RESPOND", "returned honest 'I don't have that' reply"))
            return AgentResult(answer, "fallback", steps, prefs=prefs, retrieval=retrieval)

        # plan == "recommend"
        if prefs:
            reply, recs = self._tool_recommend(prefs)
            steps.append(AgentStep("ACT", f"called recommender → {len(recs)} picks"))
            steps.append(AgentStep("CHECK", "taste terms present → recommendations are valid"))
            steps.append(AgentStep("RESPOND", "returned recommendations"))
            return AgentResult(reply, "recommend", steps, prefs=prefs, recommendations=recs)

        # Reflection: no taste parsed. Maybe it's a question we can ground after all.
        answer, retrieval = self._tool_knowledge(text)
        src = retrieval.hits[0].source if retrieval.hits else None
        steps.append(AgentStep(
            "ACT", f"no taste parsed; tried knowledge retriever → grounded={retrieval.grounded}, "
                   f"score={retrieval.score:.2f}, top_source={src}"))
        if retrieval.grounded:
            steps.append(AgentStep("CHECK", "retrieval is grounded → RE-ROUTE to knowledge answer"))
            steps.append(AgentStep("RESPOND", "returned document-grounded answer"))
            return AgentResult(answer, "knowledge", steps, prefs=prefs, retrieval=retrieval)
        steps.append(AgentStep("CHECK", "no taste and nothing grounded → ask the user to rephrase"))
        steps.append(AgentStep("RESPOND", "returned guidance hint"))
        return AgentResult(EMPTY_HINT, "fallback", steps, prefs=prefs, retrieval=retrieval)


def format_trace(result: AgentResult) -> str:
    """Render a result's steps as a compact, readable trace (for logs/UI)."""
    return "\n".join(f"{i}. [{s.name}] {s.detail}" for i, s in enumerate(result.steps, 1))


def _main() -> None:
    """Run the agent on a query and print its reasoning trace + reply."""
    import sys

    if len(sys.argv) < 2:
        print('usage: python src/agent.py "your message"')
        return
    agent = Agent()
    result = agent.run(" ".join(sys.argv[1:]))
    print(f"intent: {result.intent}")
    print("trace:")
    print(format_trace(result))
    print("\nreply:")
    print(result.reply)


if __name__ == "__main__":
    _main()
