"""
Tests for the knowledge-base retriever (src/knowledge_base.py, RAG enhancement).

Covers chunking, keyword-overlap ranking, the grounding threshold that lets the
system refuse unsupported questions, and the honest fallback answer.
"""

import pytest

from src.knowledge_base import (
    Chunk,
    _content_words,
    _split_into_chunks,
    load_knowledge,
    retrieve,
    answer_question,
    RELEVANCE_THRESHOLD,
)


# A small inline corpus so tests don't depend on the shipped docs.
DOC = """# Glossary

## Lofi
Lofi is relaxed downtempo music good for studying and focus.

## Metal
Metal is loud, aggressive, high-energy music with distorted guitars.
"""


@pytest.fixture(scope="module")
def chunks():
    return _split_into_chunks("glossary.md", DOC)


def test_split_produces_one_chunk_per_heading(chunks):
    headings = {c.heading for c in chunks}
    assert "Lofi" in headings and "Metal" in headings


def test_content_words_drops_stopwords_and_short_tokens():
    words = _content_words("What is the lofi?")
    assert "lofi" in words
    assert "the" not in words and "is" not in words


def test_retrieve_ranks_matching_heading_first(chunks):
    result = retrieve("what is lofi", chunks)
    assert result.hits[0].heading == "Lofi"
    assert result.grounded is True


def test_retrieve_distinguishes_between_sections(chunks):
    result = retrieve("tell me about metal guitars", chunks)
    assert result.hits[0].heading == "Metal"


def test_unrelated_question_is_not_grounded(chunks):
    result = retrieve("what is the capital of France", chunks)
    assert result.grounded is False
    assert result.score < RELEVANCE_THRESHOLD


def test_answer_question_grounded_returns_body(chunks):
    answer, result = answer_question("what is lofi", chunks)
    assert result.grounded is True
    assert "downtempo" in answer.lower()


def test_answer_question_ungrounded_is_honest(chunks):
    answer, result = answer_question("how do I file my taxes", chunks)
    assert result.grounded is False
    assert "don't have that" in answer.lower()


# --- Against the real shipped docs -----------------------------------------
def test_real_docs_load_and_answer_lofi():
    real_chunks = load_knowledge()
    assert len(real_chunks) > 5
    answer, result = answer_question("what is lofi?", real_chunks)
    assert result.grounded is True
    assert result.hits[0].source == "genres.md"
