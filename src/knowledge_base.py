"""
Document retrieval over the MoodMatch knowledge base (RAG enhancement).

This is the "retrieve" half of the RAG pattern from the course notebook, pointed
at a SECOND data source: the fact documents in data/knowledge/*.md (the catalog
data/songs.csv is the first source). It lets the chat answer *questions about*
music and about the recommender ("what is lofi?", "how are recommendations
scored?") instead of only returning song lists.

The retriever is deliberately a keyword search (content-word overlap with
stopwords removed), which needs no embeddings, no model download, and no API key
-- the notebook's own lesson is that "the retriever is a slot", and keyword search
is a valid thing to put in it. A relevance threshold makes the system say "I don't
have that information" rather than return an unrelated chunk (faithfulness).
"""

import glob
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Glue words that carry no topical meaning; dropped before overlap scoring.
STOPWORDS = {
    "a", "an", "the", "and", "or", "to", "for", "at", "of", "in", "on", "is",
    "are", "am", "be", "was", "were", "do", "does", "did", "how", "what", "why",
    "who", "when", "where", "which", "it", "its", "this", "that", "these", "those",
    "me", "my", "i", "you", "your", "we", "our", "with", "about", "can", "could",
    "would", "should", "will", "tell", "explain", "mean", "means", "vs", "versus",
}

DEFAULT_DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge")

# A chunk needs at least this much query overlap (matched content words as a
# fraction of the query's content words) to count as a real answer.
RELEVANCE_THRESHOLD = 0.30


@dataclass
class Chunk:
    """One retrievable passage: its source file, a human-readable heading, and text."""
    source: str
    heading: str
    text: str


@dataclass
class Retrieval:
    """Result of a knowledge query: the best chunk(s) and the top score."""
    hits: List[Chunk]
    score: float
    grounded: bool  # True if the top score cleared RELEVANCE_THRESHOLD


def _content_words(text: str) -> set:
    """Lowercase, split on non-alphanumerics, drop stopwords and 1-char tokens."""
    tokens = re.split(r"[^a-z0-9]+", text.lower())
    return {t for t in tokens if t and len(t) > 1 and t not in STOPWORDS}


def _split_into_chunks(source: str, text: str) -> List[Chunk]:
    """
    Split a markdown doc into chunks at '## ' headings. Each section (its heading
    plus body) becomes one chunk -- paragraph-sized, self-contained, and labeled.
    """
    chunks: List[Chunk] = []
    current_heading = source
    buffer: List[str] = []

    def flush():
        body = "\n".join(buffer).strip()
        if body:
            chunks.append(Chunk(source=source, heading=current_heading, text=body))

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            buffer = [line]
        else:
            buffer.append(line)
    flush()
    return chunks


def load_knowledge(docs_dir: str = DEFAULT_DOCS_DIR) -> List[Chunk]:
    """Load and chunk every .md file in the knowledge directory."""
    chunks: List[Chunk] = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.md"))):
        source = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            chunks.extend(_split_into_chunks(source, f.read()))
    return chunks


def _score_chunk(query_words: set, chunk: Chunk) -> float:
    """
    Relevance = fraction of the query's content words that appear in the chunk.
    Heading words count double (a section titled "Lofi" should win "what is lofi").
    """
    if not query_words:
        return 0.0
    heading_words = _content_words(chunk.heading)
    body_words = _content_words(chunk.text)
    matched = 0.0
    for w in query_words:
        if w in heading_words:
            matched += 2.0
        elif w in body_words:
            matched += 1.0
    return matched / (2.0 * len(query_words))


def retrieve(query: str, chunks: List[Chunk], top_k: int = 2) -> Retrieval:
    """
    Rank chunks by content-word overlap with the query and return the top_k. The
    result is marked `grounded` only if the best score clears the threshold, so
    the caller can refuse to answer unsupported questions.
    """
    query_words = _content_words(query)
    scored: List[Tuple[float, Chunk]] = [
        (_score_chunk(query_words, c), c) for c in chunks
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = [c for score, c in scored[:top_k] if score > 0]
    best = scored[0][0] if scored else 0.0
    return Retrieval(hits=top, score=best, grounded=best >= RELEVANCE_THRESHOLD)


def answer_question(query: str, chunks: List[Chunk]) -> Tuple[str, Retrieval]:
    """
    Produce a grounded answer string plus the underlying Retrieval (for tracing).
    If nothing clears the relevance threshold, say so honestly instead of guessing.
    """
    result = retrieve(query, chunks)
    if not result.grounded or not result.hits:
        return (
            "I don't have that in my notes. I can explain the genres and moods in "
            "the catalog, or how the recommender scores songs — try \"what is lofi?\" "
            "or \"how are recommendations scored?\".",
            result,
        )
    top = result.hits[0]
    answer = f"**{top.heading}** — {_body_after_heading(top)}"
    return answer, result


def _body_after_heading(chunk: Chunk) -> str:
    """Return the chunk body with its leading '## heading' line stripped."""
    lines = chunk.text.splitlines()
    if lines and lines[0].startswith("## "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _main() -> None:
    """Eyeball retrieval: python src/knowledge_base.py "what is lofi?"."""
    import sys

    if len(sys.argv) < 2:
        print('usage: python src/knowledge_base.py "your question"')
        return
    chunks = load_knowledge()
    query = " ".join(sys.argv[1:])
    answer, result = answer_question(query, chunks)
    print(f"query: {query!r}")
    print(f"grounded={result.grounded} score={result.score:.2f} "
          f"top_source={result.hits[0].source if result.hits else None}")
    print(f"answer: {answer}")


if __name__ == "__main__":
    _main()
