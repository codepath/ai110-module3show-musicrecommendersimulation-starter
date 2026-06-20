from src.recommender import Song, UserProfile, Recommender, score_song, load_songs

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
        target_acousticness=0.2,
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
        target_acousticness=0.2,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_genre_match_adds_correct_weight():
    user_prefs = {"genre": "pop", "mood": "sad", "energy": 0.5}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5}
    score, reasons = score_song(user_prefs, song)
    assert any("genre match" in r for r in reasons)
    assert score >= 0.40


def test_score_song_no_genre_or_mood_match_returns_energy_only():
    user_prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.5}
    song = {"genre": "rock", "mood": "intense", "energy": 0.5}
    score, reasons = score_song(user_prefs, song)
    assert not any("genre match" in r for r in reasons)
    assert not any("mood match" in r for r in reasons)
    assert score == round(0.25 * 1.0, 2)


def test_recommend_returns_k_results():
    rec = make_small_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_acousticness=0.2,
    )
    assert len(rec.recommend(user, k=1)) == 1
    assert len(rec.recommend(user, k=2)) == 2


def test_load_songs_returns_correct_count():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 18


def test_score_song_conflicting_profile():
    # sad mood + high energy — only one can score well
    user_prefs = {"genre": "folk", "mood": "sad", "energy": 0.9}
    sad_folk_song = {"genre": "folk", "mood": "sad", "energy": 0.3}
    intense_song = {"genre": "rock", "mood": "intense", "energy": 0.91}
    sad_score, _ = score_song(user_prefs, sad_folk_song)
    intense_score, _ = score_song(user_prefs, intense_song)
    # genre + mood match should beat pure energy match
    assert sad_score > intense_score


def test_recommend_empty_catalog():
    rec = Recommender(songs=[])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_acousticness=0.2,
    )
    assert rec.recommend(user, k=5) == []


def test_score_song_perfect_match():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, _ = score_song(user_prefs, song)
    assert score == 1.0


def test_score_song_energy_boundary():
    user_prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.0}
    song = {"genre": "jazz", "mood": "relaxed", "energy": 1.0}
    score, _ = score_song(user_prefs, song)
    # genre + mood match but energy contribution should be 0.0
    assert score == round(0.40 + 0.35 + 0.0, 3)


def test_recommend_scores_are_descending():
    songs = load_songs("data/songs.csv")
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4}
    from src.recommender import recommend_songs
    results = recommend_songs(user_prefs, songs, k=5)
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
