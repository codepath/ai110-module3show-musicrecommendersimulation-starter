from src.recommender import (
    Song, UserProfile, Recommender, load_songs, max_score, score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ---- Advanced features: popularity, decade, mood tags, language, instrumentalness ----

BASE = {"genre": "pop", "mood": "happy", "energy": 0.8}


def advanced_song(**overrides) -> dict:
    song = {
        "genre": "pop", "mood": "happy", "energy": 0.8,
        "popularity": 80, "release_decade": 2010,
        "mood_tags": ["uplifting", "bright"], "language": "english",
        "instrumentalness": 0.1,
    }
    song.update(overrides)
    return song


def test_basic_profile_scores_ignore_advanced_columns():
    plain = {"genre": "pop", "mood": "happy", "energy": 0.8}
    with_columns = advanced_song()
    without_columns = {k: with_columns[k] for k in ("genre", "mood", "energy")}
    assert score_song(plain, with_columns)[0] == score_song(plain, without_columns)[0]
    assert max_score(plain) == 4.0


def test_mood_tags_score_by_share_of_requested_tags():
    prefs = dict(BASE, mood_tags=["Uplifting", "bright", "gritty", "dark"])  # 2 of 4
    base, _ = score_song(BASE, advanced_song())
    score, reasons = score_song(prefs, advanced_song())
    assert round(score - base, 6) == 0.5  # TAG_POINTS (1.0) * 2/4
    assert any("mood tags 2/4" in r for r in reasons)


def test_popularity_and_decade_reward_closeness():
    near = score_song(dict(BASE, popularity=80), advanced_song())[0]
    far = score_song(dict(BASE, popularity=10), advanced_song())[0]
    assert near > far
    same = score_song(dict(BASE, decade=2010), advanced_song())[0]
    apart = score_song(dict(BASE, decade=1980), advanced_song())[0]
    assert same > apart
    # 30 or more years apart earns no decade points at all
    assert score_song(dict(BASE, decade=1970), advanced_song())[0] == score_song(BASE, advanced_song())[0]


def test_language_match_is_case_insensitive_and_instrumentalness_is_clamped():
    base = score_song(BASE, advanced_song())[0]
    assert round(score_song(dict(BASE, language="ENGLISH"), advanced_song())[0] - base, 6) == 0.5
    assert score_song(dict(BASE, language="spanish"), advanced_song())[0] == base
    assert score_song(dict(BASE, instrumentalness=-5), advanced_song())[0] == \
        score_song(dict(BASE, instrumentalness=0), advanced_song())[0]


def test_scores_never_exceed_max_score_with_all_advanced_prefs():
    prefs = dict(BASE, popularity=80, decade=2010, language="english",
                 mood_tags=["uplifting", "bright"], instrumentalness=0.1)
    score, _ = score_song(prefs, advanced_song())
    assert max_score(prefs) == 7.0
    assert abs(score - 7.0) < 1e-9  # a perfect match hits the ceiling exactly


def test_song_missing_advanced_values_is_skipped_not_crashed():
    prefs = dict(BASE, popularity=80, decade=2010, language="english", mood_tags=["x"])
    bare = {"genre": "pop", "mood": "happy", "energy": 0.8}
    assert score_song(prefs, bare)[0] == score_song(BASE, bare)[0]


def test_user_profile_advanced_preferences_change_the_ranking():
    quiet = Song(id=1, title="Quiet", artist="A", genre="pop", mood="happy", energy=0.8,
                 tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5,
                 popularity=20, mood_tags=["calm"])
    loud = Song(id=2, title="Hit", artist="B", genre="pop", mood="happy", energy=0.8,
                tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5,
                popularity=95, mood_tags=["euphoric"])
    rec = Recommender([quiet, loud])
    plain = UserProfile("pop", "happy", 0.8, False)
    fan = UserProfile("pop", "happy", 0.8, False, target_popularity=95,
                      preferred_mood_tags=["euphoric"])
    assert rec.recommend(fan, k=1)[0].title == "Hit"
    assert rec.recommend(plain, k=2)[0].title == "Quiet"  # tie keeps catalog order


def test_load_songs_parses_the_advanced_columns():
    songs = load_songs("data/songs.csv")
    first = songs[0]
    assert isinstance(first["popularity"], int) and 0 <= first["popularity"] <= 100
    assert isinstance(first["release_decade"], int) and first["release_decade"] % 10 == 0
    assert isinstance(first["mood_tags"], list) and len(first["mood_tags"]) >= 2
    assert isinstance(first["instrumentalness"], float)
    assert all(s["language"] for s in songs)
