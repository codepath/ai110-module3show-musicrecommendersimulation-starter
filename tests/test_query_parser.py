"""
Tests for the natural-language query parser (src/query_parser.py).

The parser turns free text into the user_prefs dict the recommender consumes.
These tests exercise genre/mood detection (including multi-word, hyphenated and
synonym terms), substring safety, energy cues, acoustic negation, the
detected-keys-only contract, and one integration test through the real scorer.
"""

import pytest

from src.query_parser import build_vocab, parse_query, parse_query_from_catalog
from src.recommender import recommend_songs


# --- Fixture catalog -------------------------------------------------------
# Genres: pop, indie pop, lofi, rock, metal, EDM, R&B, hip hop, classical,
# reggae, folk. Moods: happy, chill, intense, aggressive, dark, melancholic.
CATALOG = [
    {"id": 1, "title": "Pop Star", "artist": "A", "genre": "pop", "mood": "happy",
     "energy": 0.8, "tempo_bpm": 120, "valence": 0.8, "danceability": 0.8, "acousticness": 0.2},
    {"id": 2, "title": "Indie Twin", "artist": "B", "genre": "indie pop", "mood": "happy",
     "energy": 0.76, "tempo_bpm": 118, "valence": 0.78, "danceability": 0.79, "acousticness": 0.35},
    {"id": 3, "title": "Lofi Loop", "artist": "C", "genre": "lofi", "mood": "chill",
     "energy": 0.35, "tempo_bpm": 78, "valence": 0.55, "danceability": 0.6, "acousticness": 0.85},
    {"id": 4, "title": "Rock Wall", "artist": "D", "genre": "rock", "mood": "intense",
     "energy": 0.9, "tempo_bpm": 150, "valence": 0.45, "danceability": 0.6, "acousticness": 0.1},
    {"id": 5, "title": "Metal Storm", "artist": "E", "genre": "metal", "mood": "aggressive",
     "energy": 0.97, "tempo_bpm": 168, "valence": 0.3, "danceability": 0.4, "acousticness": 0.05},
    {"id": 6, "title": "EDM Pulse", "artist": "F", "genre": "EDM", "mood": "dark",
     "energy": 0.9, "tempo_bpm": 128, "valence": 0.38, "danceability": 0.85, "acousticness": 0.05},
    {"id": 7, "title": "Velvet Voice", "artist": "G", "genre": "R&B", "mood": "romantic",
     "energy": 0.55, "tempo_bpm": 76, "valence": 0.7, "danceability": 0.74, "acousticness": 0.4},
    {"id": 8, "title": "City Rhymes", "artist": "H", "genre": "hip hop", "mood": "energetic",
     "energy": 0.85, "tempo_bpm": 98, "valence": 0.72, "danceability": 0.86, "acousticness": 0.08},
    {"id": 9, "title": "Sad Piano", "artist": "I", "genre": "classical", "mood": "melancholic",
     "energy": 0.2, "tempo_bpm": 66, "valence": 0.2, "danceability": 0.2, "acousticness": 0.95},
    {"id": 10, "title": "Paper Sails", "artist": "J", "genre": "folk", "mood": "dreamy",
     "energy": 0.38, "tempo_bpm": 84, "valence": 0.6, "danceability": 0.45, "acousticness": 0.88},
]


@pytest.fixture(scope="module")
def vocab():
    """Build the (genre_phrases, mood_phrases) vocab once for the module."""
    return build_vocab(CATALOG)


def parse(text, vocab):
    """Thin helper: parse ``text`` against the fixture vocab."""
    genre_phrases, mood_phrases = vocab
    return parse_query(text, genre_phrases, mood_phrases)


# --- Genre detection -------------------------------------------------------
def test_detects_exact_catalog_genre(vocab):
    assert parse("I love rock music", vocab)["genre"] == "rock"


def test_detects_multiword_genre_over_substring(vocab):
    # "indie pop" must win over the bare "pop" it contains.
    assert parse("some indie pop please", vocab)["genre"] == "indie pop"


def test_detects_hyphenated_synonym_genre(vocab):
    # "k-pop" is a GENRE_SYNONYMS key, passed through raw for the scorer to remap.
    assert parse("k-pop vibes tonight", vocab)["genre"] == "k-pop"


def test_rnb_ampersand_genre_resolves_to_catalog_label(vocab):
    # "R&B" is a catalog label here, so it stores the canonical label.
    assert parse("in the mood for r&b", vocab)["genre"] == "R&B"


def test_multiword_hip_hop_genre(vocab):
    assert parse("give me hip hop", vocab)["genre"] == "hip hop"


def test_substring_does_not_match_partial_word(vocab):
    # "popcorn" must not match "pop"; "metallica" must not match "metal".
    assert "genre" not in parse("I ate popcorn at the metallica show reference", vocab)


def test_first_genre_wins_on_multiple(vocab):
    assert parse("rock or metal, either works", vocab)["genre"] == "rock"


# --- Mood detection --------------------------------------------------------
def test_detects_catalog_mood(vocab):
    assert parse("something happy", vocab)["mood"] == "happy"


def test_detects_mood_synonym(vocab):
    # "sad" is a MOOD_SYNONYMS key (scorer remaps it to melancholic).
    assert parse("feeling kind of sad", vocab)["mood"] == "sad"


# --- Energy cues -----------------------------------------------------------
def test_high_energy_cue(vocab):
    assert parse("high energy workout playlist", vocab)["energy"] == pytest.approx(0.9)


def test_low_energy_cue(vocab):
    assert parse("calm music to study to", vocab)["energy"] == pytest.approx(0.3)


def test_moderate_energy_cue(vocab):
    assert parse("something moderate tempo", vocab)["energy"] == pytest.approx(0.5)


def test_no_energy_cue_leaves_key_absent(vocab):
    assert "energy" not in parse("some jazz", vocab)


def test_conflicting_energy_cues_average(vocab):
    energy = parse("a chill workout mix", vocab)["energy"]
    assert 0.3 < energy < 0.9


# --- Acoustic detection ----------------------------------------------------
def test_detects_acoustic(vocab):
    assert parse("acoustic set please", vocab)["likes_acoustic"] is True


def test_detects_unplugged_as_acoustic(vocab):
    assert parse("something unplugged", vocab)["likes_acoustic"] is True


def test_negated_acoustic(vocab):
    assert parse("rock but not acoustic", vocab)["likes_acoustic"] is False


def test_acoustic_absent_key_omitted(vocab):
    assert "likes_acoustic" not in parse("upbeat pop", vocab)


# --- Robustness & contract -------------------------------------------------
def test_case_and_punctuation_insensitive(vocab):
    prefs = parse("CHILL, LoFi!!!", vocab)
    assert prefs["genre"] == "lofi"
    # "chill" is both a mood and a low-energy cue.
    assert prefs["mood"] == "chill"
    assert prefs["energy"] == pytest.approx(0.3)


def test_empty_or_noise_returns_empty_dict(vocab):
    assert parse("asdf qwerty zxcv", vocab) == {}
    assert parse("", vocab) == {}


def test_only_detected_keys_present(vocab):
    # "chill lofi" -> genre + mood + energy(from "chill"), and nothing else.
    prefs = parse("chill lofi", vocab)
    assert set(prefs) == {"genre", "mood", "energy"}


def test_convenience_wrapper_builds_vocab():
    prefs = parse_query_from_catalog("high-energy metal", CATALOG)
    assert prefs["genre"] == "metal"
    assert prefs["energy"] == pytest.approx(0.9)


# --- Integration through the real scorer -----------------------------------
def test_parsed_prefs_flow_through_recommender(vocab):
    prefs = parse("chill lofi for studying", vocab)
    recs = recommend_songs(prefs, CATALOG, k=3)
    top_song = recs[0][0]
    assert top_song["title"] == "Lofi Loop"
