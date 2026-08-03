"""
Tests for the music recommender.

Covers the core scoring/ranking behavior plus the five refinements added on top
of the starter logic:
  1. Out-of-vocabulary genre/mood resolved via synonyms onto real centroids.
  2. Honest caveats when a stated preference cannot be met.
  3. Fallback matches described as an audio-profile match, not a genre match.
  4. A normalized score ceiling that excludes unmatchable terms.
  5. Genre-appropriate wording for the non-acoustic ("produced") sound.
"""

import pytest

from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    recommend_songs,
    score_song,
    score_ceiling,
    GENRE_WEIGHT,
    MOOD_WEIGHT,
    ENERGY_WEIGHT,
    ACOUSTIC_WEIGHT,
)


# --- Shared fixtures -------------------------------------------------------
# A small, controlled catalog. Genres present: pop, indie pop, lofi, rock,
# metal, EDM, classical, reggae. Moods present: happy, chill, intense,
# aggressive, dark, melancholic, uplifting. "Pop Star" and "Indie Twin" share
# an identical (tempo, valence, danceability) vector so genre similarity
# between them is exactly 1.0 -- handy for testing the fallback path.
CATALOG = [
    {"id": 1, "title": "Pop Star", "artist": "A", "genre": "pop", "mood": "happy",
     "energy": 0.8, "tempo_bpm": 120, "valence": 0.8, "danceability": 0.8, "acousticness": 0.2},
    {"id": 2, "title": "Indie Twin", "artist": "B", "genre": "indie pop", "mood": "happy",
     "energy": 0.76, "tempo_bpm": 120, "valence": 0.8, "danceability": 0.8, "acousticness": 0.35},
    {"id": 3, "title": "Lofi Loop", "artist": "C", "genre": "lofi", "mood": "chill",
     "energy": 0.35, "tempo_bpm": 78, "valence": 0.55, "danceability": 0.6, "acousticness": 0.85},
    {"id": 4, "title": "Rock Wall", "artist": "D", "genre": "rock", "mood": "intense",
     "energy": 0.9, "tempo_bpm": 150, "valence": 0.45, "danceability": 0.6, "acousticness": 0.1},
    {"id": 5, "title": "Metal Storm", "artist": "E", "genre": "metal", "mood": "aggressive",
     "energy": 0.97, "tempo_bpm": 168, "valence": 0.3, "danceability": 0.4, "acousticness": 0.05},
    {"id": 6, "title": "EDM Pulse", "artist": "F", "genre": "EDM", "mood": "dark",
     "energy": 0.9, "tempo_bpm": 128, "valence": 0.38, "danceability": 0.85, "acousticness": 0.05},
    {"id": 7, "title": "Sad Piano", "artist": "G", "genre": "classical", "mood": "melancholic",
     "energy": 0.2, "tempo_bpm": 66, "valence": 0.2, "danceability": 0.2, "acousticness": 0.95},
    {"id": 8, "title": "Reggae Sun", "artist": "H", "genre": "reggae", "mood": "uplifting",
     "energy": 0.6, "tempo_bpm": 92, "valence": 0.85, "danceability": 0.78, "acousticness": 0.3},
]


def song_by_title(title):
    """Return the catalog dict with this title."""
    return next(s for s in CATALOG if s["title"] == title)


def reasons_text(reasons):
    """Join a reasons/caveats list into one lowercase string for substring checks."""
    return " | ".join(reasons).lower()


# --- Original starter tests (kept) -----------------------------------------
def make_small_recommender() -> Recommender:
    songs = [
        Song(id=1, title="Test Pop Track", artist="Test Artist", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist", genre="lofi", mood="chill",
             energy=0.4, tempo_bpm=80, valence=0.6, danceability=0.5, acousticness=0.9),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- load_songs ------------------------------------------------------------
def test_load_songs_parses_types_and_count(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Song One,Artist,pop,happy,0.8,120,0.7,0.6,0.2\n"
        "2,Song Two,Artist,lofi,chill,0.3,80,0.5,0.4,0.9\n"
    )
    songs = load_songs(str(csv_path))

    assert len(songs) == 2
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)
    assert songs[0]["title"] == "Song One"


# --- Core scoring ----------------------------------------------------------
def test_exact_genre_and_mood_earn_full_weight():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    score, reasons = score_song(prefs, song_by_title("Pop Star"), CATALOG)
    # genre 3 + mood 2 + energy 2*(1-0) + acoustic 1*(1-0.2) = 7.8
    assert score == pytest.approx(GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + 0.8)
    text = reasons_text(reasons)
    assert "matches your favorite genre" in text
    assert "fits the happy mood" in text


def test_energy_term_rewards_closeness():
    # Only energy expressed; likes_acoustic defaults False.
    near = score_song({"energy": 0.5}, song_by_title("Reggae Sun"), CATALOG)[0]  # energy 0.6
    far = score_song({"energy": 0.5}, song_by_title("Metal Storm"), CATALOG)[0]  # energy 0.97
    assert near > far


def test_unknown_labels_score_only_energy_and_acoustic():
    prefs = {"genre": "polka", "mood": "chaotic", "energy": 0.5, "likes_acoustic": False}
    score, reasons = score_song(prefs, song_by_title("Pop Star"), CATALOG)
    # genre 0 + mood 0 + energy 2*(1-0.3) + acoustic 1*(1-0.2) = 2.2
    assert score == pytest.approx(ENERGY_WEIGHT * 0.7 + ACOUSTIC_WEIGHT * 0.8)
    text = reasons_text(reasons)
    assert "matches your favorite genre" not in text
    assert "fits the" not in text


# --- Feature 1: synonym resolution -----------------------------------------
def test_synonym_genre_kpop_resolves_to_pop():
    prefs = {"genre": "k-pop", "energy": 0.8, "likes_acoustic": False}
    score, reasons = score_song(prefs, song_by_title("Pop Star"), CATALOG)
    text = reasons_text(reasons)
    # k-pop -> pop, so a pop song is an exact match worth full genre weight.
    assert 'matches your favorite genre' in text
    assert 'interpreted from "k-pop"' in text
    assert score >= GENRE_WEIGHT


def test_synonym_mood_sad_resolves_to_melancholic():
    prefs = {"mood": "sad", "energy": 0.2, "likes_acoustic": True}
    score, reasons = score_song(prefs, song_by_title("Sad Piano"), CATALOG)
    text = reasons_text(reasons)
    assert "fits the melancholic" in text
    assert 'interpreted from "sad"' in text
    assert score >= MOOD_WEIGHT


def test_truly_unknown_label_is_not_remapped():
    prefs = {"genre": "polka", "energy": 0.5}
    _, reasons = score_song(prefs, song_by_title("Pop Star"), CATALOG)
    text = reasons_text(reasons)
    assert "interpreted from" not in text
    assert 'nothing tagged "polka"' in text


# --- Feature 2: honest caveats ---------------------------------------------
def test_acoustic_preference_unmet_is_disclosed():
    prefs = {"genre": "EDM", "mood": "dark", "energy": 0.9, "likes_acoustic": True}
    _, reasons = score_song(prefs, song_by_title("EDM Pulse"), CATALOG)
    text = reasons_text(reasons)
    assert "note:" in text
    assert "isn't an acoustic track" in text


def test_unknown_genre_and_mood_are_disclosed():
    prefs = {"genre": "polka", "mood": "chaotic", "energy": 0.5}
    _, reasons = score_song(prefs, song_by_title("Reggae Sun"), CATALOG)
    text = reasons_text(reasons)
    assert 'nothing tagged "polka"' in text
    assert 'no "chaotic" mood' in text


def test_explain_recommendation_includes_caveat():
    songs = [Song(**s) for s in CATALOG]
    rec = Recommender(songs)
    user = UserProfile(favorite_genre="EDM", favorite_mood="dark",
                       target_energy=0.9, likes_acoustic=True)
    edm = next(s for s in songs if s.title == "EDM Pulse")
    explanation = rec.explain_recommendation(user, edm).lower()
    assert "note:" in explanation
    assert "isn't an acoustic track" in explanation


# --- Feature 3: honest fallback wording ------------------------------------
def test_fallback_match_uses_audio_profile_wording():
    # Ask for pop; Indie Twin shares pop's exact similarity vector -> strong,
    # non-exact match that should be described honestly.
    prefs = {"genre": "pop", "energy": 0.76, "likes_acoustic": False}
    _, reasons = score_song(prefs, song_by_title("Indie Twin"), CATALOG)
    text = reasons_text(reasons)
    assert "similar audio profile" in text
    # Regression: the old, over-claiming wording must be gone.
    assert "sounds similar to your favorite genre" not in text


def test_no_recommendation_uses_old_genre_wording():
    prefs = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}
    results = recommend_songs(prefs, CATALOG, k=len(CATALOG))
    for _, _, explanation in results:
        assert "sounds similar to your favorite genre" not in explanation.lower()


# --- Feature 4: normalized score ceiling -----------------------------------
def test_score_ceiling_full_when_everything_matchable():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    ceiling = score_ceiling(prefs, CATALOG)
    assert ceiling == pytest.approx(GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT)


def test_score_ceiling_excludes_unmatchable_terms():
    prefs = {"genre": "polka", "mood": "chaotic", "energy": 0.5, "likes_acoustic": False}
    ceiling = score_ceiling(prefs, CATALOG)
    # Only energy + acoustic can score.
    assert ceiling == pytest.approx(ENERGY_WEIGHT + ACOUSTIC_WEIGHT)


def test_score_ceiling_counts_resolved_synonyms():
    prefs = {"genre": "k-pop", "energy": 0.5}
    ceiling = score_ceiling(prefs, CATALOG)
    # k-pop resolves to pop, so the genre term counts; no mood requested.
    assert ceiling == pytest.approx(GENRE_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT)


def test_score_never_exceeds_ceiling():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    ceiling = score_ceiling(prefs, CATALOG)
    for _, score, _ in recommend_songs(prefs, CATALOG, k=len(CATALOG)):
        assert score <= ceiling + 1e-9


# --- Feature 5: genre-aware sound phrasing ---------------------------------
def test_heavy_genre_gets_heavy_phrasing():
    prefs = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}
    _, reasons = score_song(prefs, song_by_title("Rock Wall"), CATALOG)
    assert "amplified, heavy sound" in reasons_text(reasons)


def test_electronic_genre_gets_electronic_phrasing():
    prefs = {"genre": "EDM", "mood": "dark", "energy": 0.9, "likes_acoustic": False}
    _, reasons = score_song(prefs, song_by_title("EDM Pulse"), CATALOG)
    assert "produced/electronic sound" in reasons_text(reasons)


def test_other_genre_gets_clean_phrasing():
    prefs = {"energy": 0.6, "likes_acoustic": False}
    _, reasons = score_song(prefs, song_by_title("Reggae Sun"), CATALOG)  # reggae, acoustic 0.3
    assert "clean, produced sound" in reasons_text(reasons)


# --- recommend_songs / API shape -------------------------------------------
def test_recommend_songs_shape_sorted_and_respects_k():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    results = recommend_songs(prefs, CATALOG, k=3)
    assert len(results) == 3
    for item in results:
        song, score, explanation = item
        assert isinstance(song, dict)
        assert isinstance(score, float)
        assert isinstance(explanation, str)
    scores = [s for _, s, _ in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_top_pick_is_exact_match():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    top_song, _, _ = recommend_songs(prefs, CATALOG, k=1)[0]
    assert top_song["title"] == "Pop Star"


def test_recommend_songs_empty_catalog_returns_empty():
    assert recommend_songs({"genre": "pop"}, [], k=5) == []


def test_functional_and_oop_agree_on_top_pick():
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    func_top = recommend_songs(prefs, CATALOG, k=1)[0][0]["title"]

    songs = [Song(**s) for s in CATALOG]
    user = UserProfile(favorite_genre="lofi", favorite_mood="chill",
                       target_energy=0.35, likes_acoustic=True)
    oop_top = Recommender(songs).recommend(user, k=1)[0].title

    assert func_top == oop_top == "Lofi Loop"


def test_score_song_returns_two_tuple():
    result = score_song({"genre": "pop"}, song_by_title("Pop Star"), CATALOG)
    assert isinstance(result, tuple) and len(result) == 2
    _, reasons = result
    assert isinstance(reasons, list)


# --- Centroid / similarity math, observed through the public API -----------
# The similarity machinery is internal, but its effect is visible in the genre
# fallback term: for a non-exact match, genre_term = GENRE_WEIGHT * similarity^2.
# We isolate that term by zeroing the others: no mood, no energy target, and a
# known acoustic contribution.
def genre_term(genre, song):
    """Recover just the genre contribution of score_song for one song."""
    score, _ = score_song({"genre": genre, "likes_acoustic": False}, song, CATALOG)
    acoustic_term = ACOUSTIC_WEIGHT * (1.0 - song["acousticness"])
    return score - acoustic_term


def test_song_matching_a_centroid_earns_full_fallback_credit():
    # 'pop' has one song (Pop Star). 'Indie Twin' is a different genre but shares
    # Pop Star's exact (tempo, valence, danceability) vector, so it sits right on
    # the pop centroid -> similarity 1.0 -> full genre weight, even without an
    # exact genre match. This confirms both similarity==1 at the centroid and
    # that a single-song centroid equals that song.
    assert genre_term("pop", song_by_title("Indie Twin")) == pytest.approx(GENRE_WEIGHT)


def test_fallback_credit_stays_within_weight_bounds():
    # similarity in [0,1] (squared) means the genre term never leaves [0, weight].
    for s in CATALOG:
        term = genre_term("pop", s)
        assert -1e-9 <= term <= GENRE_WEIGHT + 1e-9


def test_closer_song_earns_more_fallback_credit():
    close = genre_term("pop", song_by_title("Indie Twin"))  # on the centroid
    far = genre_term("pop", song_by_title("Sad Piano"))      # far from it
    assert close > far


def test_every_catalog_genre_is_matchable():
    # If every genre has a centroid, each is usable as a preference and counts
    # toward the ceiling (genre + acoustic, since no mood/energy are given).
    for genre in {s["genre"] for s in CATALOG}:
        assert score_ceiling({"genre": genre}, CATALOG) == pytest.approx(GENRE_WEIGHT + ACOUSTIC_WEIGHT)


def test_every_catalog_mood_is_matchable():
    for mood in {s["mood"] for s in CATALOG}:
        assert score_ceiling({"mood": mood}, CATALOG) == pytest.approx(MOOD_WEIGHT + ACOUSTIC_WEIGHT)
