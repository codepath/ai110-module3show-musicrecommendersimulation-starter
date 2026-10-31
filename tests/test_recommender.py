import pytest

from src.recommender import (
    DEFAULT_DIVERSITY, DEFAULT_STRATEGY, ENERGY_FOCUSED, GENRE_FIRST, MOOD_FIRST,
    STRATEGIES, DiversityPenalty,
    Song, UserProfile, Recommender, get_strategy, load_songs, max_score,
    recommend_songs, score_song,
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


# ---- Ranking strategies (Genre-First, Mood-First, Energy-Focused) ----

def two_songs():
    genre_song = {"title": "Genre Match", "genre": "rock", "mood": "calm", "energy": 0.5}
    mood_song = {"title": "Mood Match", "genre": "jazz", "mood": "intense", "energy": 0.5}
    return [genre_song, mood_song]


def test_every_strategy_adds_up_to_four_points():
    assert set(STRATEGIES) == {"genre-first", "mood-first", "energy-focused"}
    for strategy in STRATEGIES.values():
        assert strategy.core_max == 4.0
        assert max_score(BASE, strategy) == 4.0


def test_default_strategy_is_energy_focused_and_scores_are_unchanged():
    assert DEFAULT_STRATEGY is ENERGY_FOCUSED
    song = {"genre": "pop", "mood": "happy", "energy": 0.82}
    assert score_song(BASE, song) == score_song(BASE, song, ENERGY_FOCUSED)


def test_switching_strategy_changes_which_song_wins():
    prefs = {"genre": "rock", "mood": "intense", "energy": 0.5}
    songs = two_songs()
    assert recommend_songs(prefs, songs, 1, GENRE_FIRST)[0][0]["title"] == "Genre Match"
    assert recommend_songs(prefs, songs, 1, MOOD_FIRST)[0][0]["title"] == "Mood Match"


def test_strategy_changes_the_points_shown_in_the_reasons():
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    _, genre_reasons = score_song(BASE, song, GENRE_FIRST)
    _, mood_reasons = score_song(BASE, song, MOOD_FIRST)
    assert "genre match: pop (+2.0)" in genre_reasons
    assert "mood match: happy (+2.0)" in mood_reasons


def test_get_strategy_accepts_loose_names_and_rejects_unknown_ones():
    assert get_strategy(" Mood_First ") is MOOD_FIRST
    with pytest.raises(ValueError, match="Choose from"):
        get_strategy("vibes-only")


def test_recommender_class_uses_the_strategy_it_is_given():
    rock = Song(id=1, title="Rock", artist="A", genre="rock", mood="calm", energy=0.5,
                tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5)
    jazz = Song(id=2, title="Jazz", artist="B", genre="jazz", mood="intense", energy=0.5,
                tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5)
    user = UserProfile("rock", "intense", 0.5, False)
    assert Recommender([rock, jazz], GENRE_FIRST).recommend(user, k=1)[0].title == "Rock"
    assert Recommender([rock, jazz], MOOD_FIRST).recommend(user, k=1)[0].title == "Jazz"


# ---- Diversity penalty (repeat artists and genres) ----

# Target energy 0.5 with no genre/mood match, so a song's score is 2 * (1 - gap).
DIV_PREFS = {"genre": "none", "mood": "none", "energy": 0.5}


def div_song(title, artist, genre, energy):
    return {"title": title, "artist": artist, "genre": genre, "mood": "x", "energy": energy}


def titles(results):
    return [song["title"] for song, _, _ in results]


def test_no_penalty_means_the_plain_top_scores():
    songs = [div_song("A1", "X", "g", 0.5), div_song("A2", "X", "g", 0.6),
             div_song("B", "Y", "h", 0.7)]
    assert titles(recommend_songs(DIV_PREFS, songs, 3)) == ["A1", "A2", "B"]


def test_repeat_artist_is_pushed_below_a_different_artist():
    songs = [div_song("A1", "X", "g", 0.5), div_song("A2", "X", "h", 0.6),
             div_song("B", "Y", "i", 0.7)]
    penalty = DiversityPenalty(artist_penalty=0.75, genre_penalty=0.0)
    results = recommend_songs(DIV_PREFS, songs, 3, diversity=penalty)
    assert titles(results) == ["A1", "B", "A2"]
    assert any("artist X already picked 1x" in reasons for _, _, reasons in results)


def test_repeat_genre_is_pushed_below_a_different_genre():
    songs = [div_song("A1", "X", "g", 0.5), div_song("A2", "Y", "g", 0.6),
             div_song("B", "Z", "h", 0.7)]
    penalty = DiversityPenalty(artist_penalty=0.0, genre_penalty=0.25)
    assert titles(recommend_songs(DIV_PREFS, songs, 3, diversity=penalty)) == ["A1", "B", "A2"]


def test_penalty_stacks_for_each_earlier_pick_by_the_same_artist():
    songs = [div_song("A1", "X", "g", 0.5), div_song("A2", "X", "g", 0.6),
             div_song("A3", "X", "g", 0.4), div_song("C", "Z", "g", 0.75)]
    # A2 (1.8) and A3 (1.8) both beat C (1.5) with a flat 0.2 penalty. A3 only falls
    # behind C when the penalty stacks: 1.8 - 2 * 0.2 = 1.4.
    penalty = DiversityPenalty(artist_penalty=0.2, genre_penalty=0.0)
    assert titles(recommend_songs(DIV_PREFS, songs, 4, diversity=penalty)) == ["A1", "A2", "C", "A3"]


def test_first_pick_is_never_penalized_and_scores_never_go_below_zero():
    songs = [div_song("A1", "X", "g", 0.5), div_song("A2", "X", "g", 0.6)]
    harsh = DiversityPenalty(artist_penalty=5.0, genre_penalty=5.0)
    results = recommend_songs(DIV_PREFS, songs, 2, diversity=harsh)
    assert results[0][1] == recommend_songs(DIV_PREFS, songs, 1)[0][1]
    assert results[1][1] == 0.0


def test_penalized_scores_stay_within_the_normal_bounds():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    for _, score, _ in recommend_songs(prefs, songs, 5, diversity=DEFAULT_DIVERSITY):
        assert 0.0 <= score <= max_score(prefs)


def test_default_penalty_gives_the_lofi_listener_a_more_varied_list():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    plain = recommend_songs(prefs, songs, 5)
    varied = recommend_songs(prefs, songs, 5, diversity=DEFAULT_DIVERSITY)
    def most_from_one_artist(results):
        counts = {}
        for song, _, _ in results:
            counts[song["artist"]] = counts.get(song["artist"], 0) + 1
        return max(counts.values())
    assert most_from_one_artist(plain) == 2
    assert most_from_one_artist(varied) == 1


def test_recommender_class_applies_the_diversity_penalty():
    def song(sid, title, artist, genre, energy):
        return Song(id=sid, title=title, artist=artist, genre=genre, mood="x", energy=energy,
                    tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5)
    songs = [song(1, "A1", "X", "g", 0.5), song(2, "A2", "X", "h", 0.6), song(3, "B", "Y", "i", 0.7)]
    user = UserProfile("none", "none", 0.5, False)
    penalty = DiversityPenalty(artist_penalty=0.75, genre_penalty=0.0)
    assert [x.title for x in Recommender(songs).recommend(user, k=3)] == ["A1", "A2", "B"]
    assert [x.title for x in Recommender(songs, diversity=penalty).recommend(user, k=3)] == ["A1", "B", "A2"]
