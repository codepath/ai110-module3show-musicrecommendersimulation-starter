"""
Tests for the agentic workflow (src/agent.py).

Verifies the router's decisions and, importantly, the reflection/re-route step:
a "question" that grounds nothing but carries taste terms should fall through to
the recommender, and a "request" that parses no taste but grounds a doc should
fall through to the knowledge answer. Also checks that a reasoning trace is always
produced.
"""

import pytest

from src.agent import Agent, format_trace


@pytest.fixture(scope="module")
def agent():
    """Real agent over the shipped catalog + knowledge docs."""
    return Agent()


def test_knowledge_question_routes_to_docs(agent):
    result = agent.run("what is lofi?")
    assert result.intent == "knowledge"
    assert "downtempo" in result.reply.lower()
    assert result.retrieval is not None and result.retrieval.grounded


def test_taste_request_routes_to_recommender(agent):
    result = agent.run("chill lofi for studying, acoustic")
    assert result.intent == "recommend"
    assert result.recommendations and len(result.recommendations) > 0
    # Top pick should be a lofi/chill track.
    top = result.recommendations[0][0]
    assert top["genre"] == "lofi"


def test_how_it_works_question_routes_to_docs(agent):
    result = agent.run("how are recommendations scored?")
    assert result.intent == "knowledge"
    assert "weighted" in result.reply.lower() or "content-based" in result.reply.lower()


def test_reroute_question_without_grounding_but_with_taste(agent):
    # Phrased as a question, but nothing in the docs grounds "euphoric" (a mood
    # synonym); the parsed taste should trigger a RE-ROUTE to the recommender.
    result = agent.run("can you play something euphoric?")
    assert result.intent == "recommend"
    assert any(step.name == "CHECK" and "RE-ROUTE" in step.detail for step in result.steps)


def test_gibberish_falls_back_gracefully(agent):
    result = agent.run("polka chaotic gibberish")
    assert result.intent == "fallback"
    assert "couldn't pick up" in result.reply.lower() or "don't have that" in result.reply.lower()


def test_trace_is_always_populated(agent):
    for msg in ["what is metal?", "high-energy rock", "asdf qwerty"]:
        result = agent.run(msg)
        assert len(result.steps) >= 3
        names = [s.name for s in result.steps]
        assert "PLAN" in names and "RESPOND" in names
        assert format_trace(result).startswith("1. [PLAN]")
