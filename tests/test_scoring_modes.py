import pytest

from src.main import ADVANCED_PROFILES, ADVERSARIAL_PROFILES, STANDARD_PROFILES
from src.recommender import SCORING_MODES, load_songs, recommend_songs, score_song

# User wants pop, happy, mid energy. Four tiny songs, each built to win under one mode.
USER = {"genre": "pop", "mood": "happy", "energy": 0.5}
GENRE_ONLY = {"title": "Genre Only", "genre": "pop", "mood": "sad", "energy": 0.5}
MOOD_ONLY = {"title": "Mood Only", "genre": "rock", "mood": "happy", "energy": 0.5}
ENERGY_ONLY = {"title": "Energy Only", "genre": "rock", "mood": "sad", "energy": 0.5}
LABELS_ONLY = {"title": "Labels Only", "genre": "pop", "mood": "happy", "energy": 0.0}


def best(mode, songs):
    return recommend_songs(USER, songs, k=1, mode=mode)[0][0]["title"]


def test_unknown_mode_raises():
    with pytest.raises(ValueError):
        score_song(USER, GENRE_ONLY, mode="nonsense")
    with pytest.raises(ValueError):
        recommend_songs(USER, [GENRE_ONLY], mode="nonsense")


def test_default_mode_is_balanced():
    assert score_song(USER, GENRE_ONLY) == score_song(USER, GENRE_ONLY, mode="balanced")


def test_genre_first_prefers_genre_match():
    songs = [GENRE_ONLY, MOOD_ONLY]
    assert best("genre-first", songs) == "Genre Only"
    assert best("mood-first", songs) == "Mood Only"


def test_balanced_ranks_mood_above_genre():
    assert best("balanced", [GENRE_ONLY, MOOD_ONLY]) == "Mood Only"


def test_energy_focused_beats_label_matches():
    songs = [ENERGY_ONLY, LABELS_ONLY]
    assert best("energy-focused", songs) == "Energy Only"
    assert best("balanced", songs) == "Labels Only"


def test_modes_change_the_scores():
    scores = {mode: score_song(USER, GENRE_ONLY, mode)[0] for mode in SCORING_MODES}
    assert len(set(round(s, 4) for s in scores.values())) == len(SCORING_MODES)


def test_every_mode_stays_between_zero_and_one_on_every_profile():
    songs = load_songs("data/songs.csv")
    profiles = {**STANDARD_PROFILES, **ADVERSARIAL_PROFILES, **ADVANCED_PROFILES}
    for mode in SCORING_MODES:
        for prefs in profiles.values():
            for song in songs:
                score, _ = score_song(prefs, song, mode)
                assert 0.0 <= score <= 1.0


def test_recommend_returns_k_sorted_results_in_every_mode():
    songs = load_songs("data/songs.csv")
    for mode in SCORING_MODES:
        results = recommend_songs(STANDARD_PROFILES["Chill Lofi"], songs, k=4, mode=mode)
        scores = [score for _, score, _ in results]
        assert len(results) == 4
        assert scores == sorted(scores, reverse=True)


def test_reasons_add_up_to_the_score():
    songs = load_songs("data/songs.csv")
    for mode in SCORING_MODES:
        score, reasons = score_song(STANDARD_PROFILES["High-Energy Pop"], songs[0], mode)
        total = sum(float(r.rsplit("(+", 1)[1].rstrip(")")) for r in reasons)
        assert total == pytest.approx(score, abs=0.03)  # each reason is rounded to 2 places
