"""
Natural-language query parser for the Music Recommender chat interface.

Turns a free-text request like "chill lofi for studying, acoustic please" into
the structured ``user_prefs`` dict that recommender.py already understands:
``{"genre": ..., "mood": ..., "energy": 0.0-1.0, "likes_acoustic": bool}``.

Design notes:
- The genre/mood vocabulary is NOT hardcoded here. Exact labels come from the
  catalog itself and the out-of-vocabulary terms come from GENRE_SYNONYMS /
  MOOD_SYNONYMS in recommender.py, so this parser stays in sync with the scorer.
- We only ever emit keys we actually detected, so score_ceiling() in the
  recommender normalizes fairly (an un-requested term never inflates the ceiling).
- Matching is whole-word via alnum lookarounds so "popcorn" does not match "pop"
  and "metallica" does not match "metal", while "k-pop", "r&b" and "lo-fi" still do.
"""

import re
import sys
from typing import Dict, List, Optional, Tuple

# Support both `python -m src.query_parser` (package import) and
# `python src/query_parser.py` (direct import), matching src/main.py.
try:
    from src.recommender import GENRE_SYNONYMS, MOOD_SYNONYMS, load_songs
except ModuleNotFoundError:
    from recommender import GENRE_SYNONYMS, MOOD_SYNONYMS, load_songs


# --- Energy cues -----------------------------------------------------------
# Ordered high -> mid -> low. Each cue phrase votes for a target energy; when a
# query trips cues in more than one bucket we average their values (so "chill
# workout" lands in the middle rather than picking a side).
ENERGY_CUES: List[Tuple[float, List[str]]] = [
    (0.9, ["high energy", "high-energy", "pumped", "workout", "gym", "intense",
           "hype", "banger", "party", "upbeat", "fast", "hard", "energetic"]),
    (0.5, ["moderate", "medium", "mid tempo", "mid-tempo", "groovy", "steady"]),
    (0.3, ["chill", "relax", "relaxing", "study", "studying", "sleep", "sleepy",
           "calm", "mellow", "slow", "low energy", "low-energy", "background",
           "focus", "focused", "quiet"]),
]

# --- Acoustic cues ---------------------------------------------------------
ACOUSTIC_TERMS = ["acoustic", "unplugged", "organic", "stripped back", "stripped-back"]
# Negation words that flip an acoustic mention to "not acoustic" when they
# appear shortly before the acoustic term.
NEGATIONS = ["not", "no", "non", "without", "anti", "avoid", "isn't", "dont", "don't"]


def build_vocab(songs: List[Dict]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Build the genre/mood matching vocabulary from the catalog + synonym tables.

    Returns (genre_phrases, mood_phrases): each maps a lowercased phrase to the
    value to store in user_prefs. Exact catalog labels map to the canonical
    label (an exact match in the scorer); synonym-only keys map to the raw key
    so the scorer's _resolve_label remaps them (and produces the nice
    'interpreted from "..."' explanation). setdefault ensures a real catalog
    label wins if a term is both a label and a synonym key.
    """
    genre_phrases: Dict[str, str] = {}
    for s in songs:
        label = s.get("genre", "")
        if label:
            genre_phrases[label.lower()] = label
    for key in GENRE_SYNONYMS:
        genre_phrases.setdefault(key.lower(), key)

    mood_phrases: Dict[str, str] = {}
    for s in songs:
        label = s.get("mood", "")
        if label:
            mood_phrases[label.lower()] = label
    for key in MOOD_SYNONYMS:
        mood_phrases.setdefault(key.lower(), key)

    return genre_phrases, mood_phrases


def _phrase_pattern(phrase: str) -> re.Pattern:
    """
    Whole-word matcher for a phrase. Uses alnum lookarounds instead of \\b so
    that punctuation-carrying terms (k-pop, r&b, lo-fi) match, while a bare
    substring inside a larger word (popcorn, metallica) does not. Internal
    whitespace tolerates multiple spaces/newlines.
    """
    escaped = r"\s+".join(re.escape(part) for part in phrase.split())
    return re.compile(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])")


def _find_first(text: str, phrases: Dict[str, str]) -> Optional[str]:
    """
    Return the stored value of the earliest-occurring phrase in ``text``.
    Longer phrases are tried first at each position so 'indie pop' beats 'pop'
    and 'hard rock' beats 'rock'. Ties on position are broken by phrase length.
    """
    best_pos: Optional[int] = None
    best_len = -1
    best_value: Optional[str] = None
    for phrase, value in phrases.items():
        m = _phrase_pattern(phrase).search(text)
        if not m:
            continue
        pos = m.start()
        # Earliest match wins; on a tie prefer the longer (more specific) phrase.
        if best_pos is None or pos < best_pos or (pos == best_pos and len(phrase) > best_len):
            best_pos, best_len, best_value = pos, len(phrase), value
    return best_value


def _detect_energy(text: str) -> Optional[float]:
    """Average the target energies of every cue bucket the text trips, or None."""
    hits: List[float] = []
    for value, cues in ENERGY_CUES:
        if any(_phrase_pattern(cue).search(text) for cue in cues):
            hits.append(value)
    if not hits:
        return None
    return round(sum(hits) / len(hits), 3)


def _detect_acoustic(text: str) -> Optional[bool]:
    """
    True if the text asks for acoustic, False if it negates it, None if the
    topic never comes up. Negation is detected when a negation word appears in
    the ~3 tokens right before the acoustic term.
    """
    for term in ACOUSTIC_TERMS:
        m = _phrase_pattern(term).search(text)
        if not m:
            continue
        preceding = text[:m.start()].split()[-3:]
        if any(neg in preceding for neg in NEGATIONS):
            return False
        return True
    return None


def parse_query(text: str,
                genre_phrases: Dict[str, str],
                mood_phrases: Dict[str, str]) -> Dict:
    """
    Parse free text into a user_prefs dict, emitting ONLY detected keys.

    Keys (all optional): "genre", "mood", "energy" (0-1), "likes_acoustic".
    An empty dict means nothing recognizable was found; the caller decides how
    to respond (the chat app asks the user to rephrase).
    """
    lowered = (text or "").lower()
    prefs: Dict = {}

    genre = _find_first(lowered, genre_phrases)
    if genre is not None:
        prefs["genre"] = genre

    mood = _find_first(lowered, mood_phrases)
    if mood is not None:
        prefs["mood"] = mood

    energy = _detect_energy(lowered)
    if energy is not None:
        prefs["energy"] = energy

    acoustic = _detect_acoustic(lowered)
    if acoustic is not None:
        prefs["likes_acoustic"] = acoustic

    return prefs


def parse_query_from_catalog(text: str, songs: List[Dict]) -> Dict:
    """Convenience wrapper that builds the vocab from ``songs`` on the fly."""
    genre_phrases, mood_phrases = build_vocab(songs)
    return parse_query(text, genre_phrases, mood_phrases)


def _main() -> None:
    """Eyeball a parse without launching Streamlit: python src/query_parser.py "chill lofi"."""
    import os

    if len(sys.argv) < 2:
        print('usage: python src/query_parser.py "your request here"')
        return
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(data_path)
    query = " ".join(sys.argv[1:])
    print(f"query: {query!r}")
    print(f"prefs: {parse_query_from_catalog(query, songs)}")


if __name__ == "__main__":
    _main()
