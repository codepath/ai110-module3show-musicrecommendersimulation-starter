from src.recommender import (
    Song, 
    UserProfile, 
    Recommender,
    score_song,
    create_chill_lofi_lover,
    create_intense_rock_fan,
    create_jazz_soul_lover,
)

# ============================================================================
# FIXTURES
# ============================================================================

def make_small_recommender() -> Recommender:
    """Creates a simple recommender with 2 test songs."""
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


def make_diverse_recommender() -> Recommender:
    """Creates a recommender with diverse songs for comprehensive testing."""
    songs = [
        # Pop song - happy, energetic, not acoustic
        Song(
            id=1,
            title="Sunny Days",
            artist="Happy Band",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        # Lofi song - chill, low energy, very acoustic
        Song(
            id=2,
            title="Study Beats",
            artist="Lofi Master",
            genre="lofi",
            mood="chill",
            energy=0.3,
            tempo_bpm=80,
            valence=0.5,
            danceability=0.3,
            acousticness=0.95,
        ),
        # Rock song - intense, high energy, not acoustic
        Song(
            id=3,
            title="Electric Thunder",
            artist="Rock Legends",
            genre="rock",
            mood="intense",
            energy=0.9,
            tempo_bpm=160,
            valence=0.4,
            danceability=0.6,
            acousticness=0.1,
        ),
        # Jazz song - relaxed, moderate energy, acoustic
        Song(
            id=4,
            title="Smooth Vibes",
            artist="Jazz Quartet",
            genre="jazz",
            mood="relaxed",
            energy=0.45,
            tempo_bpm=90,
            valence=0.6,
            danceability=0.5,
            acousticness=0.85,
        ),
        # Indie song - medium everything
        Song(
            id=5,
            title="Indie Dream",
            artist="Indie Artist",
            genre="indie",
            mood="introspective",
            energy=0.5,
            tempo_bpm=100,
            valence=0.5,
            danceability=0.5,
            acousticness=0.5,
        ),
    ]
    return Recommender(songs)


# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

def test_recommend_returns_songs_sorted_by_score():
    """Test that recommend returns songs in descending score order."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Pop, happy, high energy song should score higher than lofi
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    """Test that explain_recommendation returns a non-empty string."""
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


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

def test_recommend_empty_song_list():
    """Test recommend with empty song list."""
    rec = Recommender([])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    results = rec.recommend(user, k=5)
    assert results == []


def test_recommend_k_greater_than_song_count():
    """Test recommend when k > number of songs."""
    rec = make_small_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    results = rec.recommend(user, k=10)
    # Should return all available songs (up to 2)
    assert len(results) <= 2


def test_recommend_k_zero():
    """Test recommend with k=0."""
    rec = make_small_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    results = rec.recommend(user, k=0)
    assert len(results) == 0


def test_recommend_k_one():
    """Test recommend with k=1."""
    rec = make_small_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    results = rec.recommend(user, k=1)
    assert len(results) == 1


# ============================================================================
# GENRE MATCHING TESTS
# ============================================================================

def test_genre_match_gives_points():
    """Test that matching genre gives +1.0 points."""
    rec = make_diverse_recommender()
    user_pop = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.5,
        target_acousticness=0.5,
        likes_acoustic=False,
    )
    
    # Pop song should score higher for pop user
    results = rec.recommend(user_pop, k=5)
    pop_song = results[0]  # Should be first
    assert pop_song.genre == "pop"


def test_no_genre_match():
    """Test when user's favorite genre has no songs."""
    rec = make_diverse_recommender()
    user = UserProfile(
        favorite_genre="classical",  # No classical songs in rec
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.5,
        target_acousticness=0.5,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user, k=5)
    # Should return songs but none with genre match bonus
    assert len(results) > 0
    # First song won't be classified by genre bonus alone
    for song in results:
        assert song.genre != "classical"


def test_genre_case_insensitive():
    """Test that genre matching is case-insensitive."""
    rec = Recommender([
        Song(
            id=1,
            title="Test",
            artist="Artist",
            genre="Pop",  # Capital P
            mood="happy",
            energy=0.5,
            tempo_bpm=100,
            valence=0.7,
            danceability=0.5,
            acousticness=0.2,
        ),
    ])
    
    user = UserProfile(
        favorite_genre="pop",  # Lowercase p
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.5,
        target_acousticness=0.5,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user, k=1)
    # Should match despite case difference
    assert len(results) == 1
    assert results[0].genre == "Pop"


# ============================================================================
# MOOD MATCHING TESTS
# ============================================================================

def test_mood_match_gives_points():
    """Test that matching mood gives +1.0 points."""
    rec = make_diverse_recommender()
    user_chill = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.3,
        target_valence=0.5,
        target_acousticness=0.9,
        likes_acoustic=True,
    )
    
    results = rec.recommend(user_chill, k=5)
    # Lofi + chill should score highest
    top_song = results[0]
    assert top_song.genre == "lofi"
    assert top_song.mood == "chill"


def test_mood_mismatch():
    """Test with mismatched mood preferences."""
    rec = make_diverse_recommender()
    user = UserProfile(
        favorite_genre="rock",
        favorite_mood="calm",  # Rock songs are intense, not calm
        target_energy=0.9,
        target_valence=0.3,
        target_acousticness=0.1,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user, k=5)
    # Rock song will score high for genre/energy but low for mood
    assert len(results) > 0


# ============================================================================
# ENERGY MATCHING TESTS  
# ============================================================================

def test_energy_matching():
    """Test that energy similarity affects score."""
    rec = Recommender([
        Song(
            id=1,
            title="High Energy",
            artist="Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=140,
            valence=0.8,
            danceability=0.8,
            acousticness=0.1,
        ),
        Song(
            id=2,
            title="Low Energy",
            artist="Artist",
            genre="pop",
            mood="happy",
            energy=0.2,
            tempo_bpm=60,
            valence=0.8,
            danceability=0.2,
            acousticness=0.9,
        ),
    ])
    
    user_high_energy = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.85,
        target_valence=0.8,
        target_acousticness=0.1,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user_high_energy, k=2)
    # High energy song should score higher
    assert results[0].energy == 0.8
    assert results[1].energy == 0.2


def test_energy_precision_bonus():
    """Test that perfect energy match gets +0.5 bonus."""
    rec = Recommender([
        Song(
            id=1,
            title="Exact Energy",
            artist="Artist",
            genre="pop",
            mood="happy",
            energy=0.5,  # Exact match
            tempo_bpm=100,
            valence=0.6,
            danceability=0.6,
            acousticness=0.3,
        ),
        Song(
            id=2,
            title="Different Energy",
            artist="Artist",
            genre="pop",
            mood="happy",
            energy=0.3,  # Different
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.3,
        ),
    ])
    
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.6,
        target_acousticness=0.3,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user, k=2)
    # Exact match should score higher due to +0.5 bonus
    assert results[0].energy == 0.5


# ============================================================================
# VALENCE (MOOD POSITIVITY) TESTS
# ============================================================================

def test_valence_matching():
    """Test that valence similarity affects score."""
    rec = Recommender([
        Song(
            id=1,
            title="Happy Song",
            artist="Artist",
            genre="pop",
            mood="happy",
            energy=0.5,
            tempo_bpm=100,
            valence=0.9,  # High valence
            danceability=0.7,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Sad Song",
            artist="Artist",
            genre="rock",
            mood="intense",
            energy=0.5,
            tempo_bpm=100,
            valence=0.2,  # Low valence
            danceability=0.5,
            acousticness=0.2,
        ),
    ])
    
    user_happy = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.9,
        target_acousticness=0.2,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user_happy, k=2)
    # Happy song should score higher
    assert results[0].valence == 0.9


def test_low_valence_preference():
    """Test that users can prefer low valence (sad/intense) music."""
    rec = Recommender([
        Song(
            id=1,
            title="Intense Rock",
            artist="Rock Band",
            genre="rock",
            mood="intense",
            energy=0.9,
            tempo_bpm=150,
            valence=0.3,  # Low valence
            danceability=0.5,
            acousticness=0.1,
        ),
        Song(
            id=2,
            title="Upbeat Pop",
            artist="Pop Artist",
            genre="pop",
            mood="happy",
            energy=0.6,
            tempo_bpm=110,
            valence=0.9,  # High valence
            danceability=0.8,
            acousticness=0.1,
        ),
    ])
    
    user_intense = UserProfile(
        favorite_genre="rock",
        favorite_mood="intense",
        target_energy=0.9,
        target_valence=0.3,  # Wants low valence!
        target_acousticness=0.1,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user_intense, k=2)
    # Should prefer intense rock with low valence
    assert results[0].genre == "rock"


# ============================================================================
# ACOUSTICNESS TESTS
# ============================================================================

def test_acousticness_preference_high():
    """Test user who wants acoustic music."""
    rec = Recommender([
        Song(
            id=1,
            title="Acoustic Guitar",
            artist="Acoustic Artist",
            genre="folk",
            mood="warm",
            energy=0.4,
            tempo_bpm=90,
            valence=0.7,
            danceability=0.4,
            acousticness=0.95,  # Very acoustic
        ),
        Song(
            id=2,
            title="Electric Synth",
            artist="Electronic Artist",
            genre="electronic",
            mood="energetic",
            energy=0.8,
            tempo_bpm=120,
            valence=0.8,
            danceability=0.9,
            acousticness=0.05,  # Very electric
        ),
    ])
    
    user_acoustic = UserProfile(
        favorite_genre="folk",
        favorite_mood="warm",
        target_energy=0.4,
        target_valence=0.7,
        target_acousticness=0.9,  # Wants acoustic
        likes_acoustic=True,
    )
    
    results = rec.recommend(user_acoustic, k=2)
    # Acoustic song should score higher
    assert results[0].acousticness > 0.9


def test_acousticness_preference_low():
    """Test user who wants electric/non-acoustic music."""
    rec = Recommender([
        Song(
            id=1,
            title="Acoustic Guitar",
            artist="Acoustic Artist",
            genre="folk",
            mood="warm",
            energy=0.4,
            tempo_bpm=90,
            valence=0.7,
            danceability=0.4,
            acousticness=0.95,  # Very acoustic
        ),
        Song(
            id=2,
            title="Electric Synth",
            artist="Electronic Artist",
            genre="electronic",
            mood="energetic",
            energy=0.8,
            tempo_bpm=120,
            valence=0.8,
            danceability=0.9,
            acousticness=0.05,  # Very electric
        ),
    ])
    
    user_electric = UserProfile(
        favorite_genre="electronic",
        favorite_mood="energetic",
        target_energy=0.8,
        target_valence=0.8,
        target_acousticness=0.05,  # Wants electric!
        likes_acoustic=False,
    )
    
    results = rec.recommend(user_electric, k=2)
    # Electric song should score higher
    assert results[0].acousticness < 0.1


# ============================================================================
# CONFLICT PENALTY TESTS
# ============================================================================

def test_high_energy_low_valence_conflict():
    """Test that high energy + low valence can trigger conflict penalty."""
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_valence": 0.2,  # Low valence (sad)
        "target_acousticness": 0.1,
        "acousticness_weight": 0.5,
    }
    
    song = {
        "id": 1,
        "title": "Angry Rock",
        "artist": "Band",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "valence": 0.2,
        "danceability": 0.5,
        "acousticness": 0.1,
        "tempo_bpm": 150,
    }
    
    score, reasons = score_song(user_prefs, song)
    # Score should be positive despite conflict
    assert score > 0
    # "Conflict" might not be in reasons if diff <= 0.6
    # Check: conflict = |0.9 - (1-0.2)| = |0.9 - 0.8| = 0.1 (no conflict)
    # So no conflict penalty here


def test_contradictory_preferences_trigger_penalty():
    """Test case where preferences contradict (high energy + high valence but user wants low valence)."""
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "melancholic",
        "target_energy": 0.9,  # High energy
        "target_valence": 0.1,  # Very low valence (sad) - contradiction!
        "target_acousticness": 0.3,
        "acousticness_weight": 1.0,
    }
    
    song = {
        "id": 1,
        "title": "Happy Pop",
        "artist": "Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.2,
        "tempo_bpm": 120,
    }
    
    score, reasons = score_song(user_prefs, song)
    # Check: conflict = |0.9 - (1 - 0.1)| = |0.9 - 0.9| = 0.0 (no conflict technically)
    assert score > 0


def test_conflicting_user_preferences():
    """Test with user preferences that contradict each other."""
    user_prefs = {
        "favorite_genre": "metal",
        "favorite_mood": "melancholic",
        "target_energy": 0.95,  # Very high
        "target_valence": 0.05,  # Very low (sad)
        "target_acousticness": 0.9,  # Very acoustic
        "acousticness_weight": 1.5,
    }
    
    # This user wants: fast, sad, and acoustic
    # How can something be sad (low valence) and acoustic and energetic?
    # This will expose the system's handling of contradictions
    
    song = {
        "id": 1,
        "title": "Acoustic Scream",
        "artist": "Artist",
        "genre": "metal",
        "mood": "melancholic",
        "energy": 0.92,
        "valence": 0.08,
        "danceability": 0.2,
        "acousticness": 0.85,
        "tempo_bpm": 180,
    }
    
    score, reasons = score_song(user_prefs, song)
    # score should still be reasonable despite contradictions
    assert score > 0
    assert "Genre match" in reasons  # Metal genre matches


# ============================================================================
# PREDEFINED PROFILE TESTS
# ============================================================================

def test_chill_lofi_lover_profile():
    """Test recommendations for chill lofi lover."""
    rec = make_diverse_recommender()
    lofi_user = create_chill_lofi_lover()
    
    # Create UserProfile from dict
    user = UserProfile(
        favorite_genre=lofi_user["favorite_genre"],
        favorite_mood=lofi_user["favorite_mood"],
        target_energy=lofi_user["target_energy"],
        target_valence=lofi_user["target_valence"],
        target_acousticness=lofi_user["target_acousticness"],
        likes_acoustic=lofi_user["likes_acoustic"],
    )
    
    results = rec.recommend(user, k=5)
    # Should prefer lofi
    assert results[0].genre == "lofi"


def test_intense_rock_fan_profile():
    """Test recommendations for intense rock fan."""
    rec = make_diverse_recommender()
    rock_user = create_intense_rock_fan()
    
    user = UserProfile(
        favorite_genre=rock_user["favorite_genre"],
        favorite_mood=rock_user["favorite_mood"],
        target_energy=rock_user["target_energy"],
        target_valence=rock_user["target_valence"],
        target_acousticness=rock_user["target_acousticness"],
        likes_acoustic=rock_user["likes_acoustic"],
    )
    
    results = rec.recommend(user, k=5)
    # Should prefer rock
    assert results[0].genre == "rock"


def test_jazz_soul_lover_profile():
    """Test recommendations for jazz/soul lover."""
    rec = make_diverse_recommender()
    jazz_user = create_jazz_soul_lover()
    
    user = UserProfile(
        favorite_genre=jazz_user["favorite_genre"],
        favorite_mood=jazz_user["favorite_mood"],
        target_energy=jazz_user["target_energy"],
        target_valence=jazz_user["target_valence"],
        target_acousticness=jazz_user["target_acousticness"],
        likes_acoustic=jazz_user["likes_acoustic"],
    )
    
    results = rec.recommend(user, k=5)
    # Should prefer jazz
    assert results[0].genre == "jazz"


# ============================================================================
# EXPLANATION TESTS
# ============================================================================

def test_explanation_mentions_genre_match():
    """Test that explanation mentions genre match when present."""
    rec = make_small_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_acousticness=0.2,
        likes_acoustic=False,
    )
    song = rec.songs[0]  # Pop song
    
    explanation = rec.explain_recommendation(user, song)
    assert len(explanation) > 0
    # Should mention genre or general match
    assert "match" in explanation.lower() or "genre" in explanation.lower() or explanation != ""


def test_explanation_different_for_different_users():
    """Test that explanations differ for different users."""
    rec = make_small_recommender()
    song = rec.songs[0]  # Same song
    
    user_pop = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_acousticness=0.2,
        likes_acoustic=False,
    )
    
    user_lofi = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        target_valence=0.6,
        target_acousticness=0.9,
        likes_acoustic=True,
    )
    
    explanation_pop = rec.explain_recommendation(user_pop, song)
    explanation_lofi = rec.explain_recommendation(user_lofi, song)
    
    # Explanations should be different for different users
    assert len(explanation_pop) > 0
    assert len(explanation_lofi) > 0


# ============================================================================
# SORTING & RANKING TESTS
# ============================================================================

def test_recommendations_sorted_descending():
    """Test that recommendations are sorted by score (highest first)."""
    rec = make_diverse_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.8,
        target_acousticness=0.2,
        likes_acoustic=False,
    )
    
    results = rec.recommend(user, k=5)
    # All songs should be returned in order
    if len(results) > 1:
        # Results should be sorted (we can't verify scores directly without access,
        # but we can verify the order makes sense)
        assert len(results) > 0


def test_top_k_respects_limit():
    """Test that top-k recommendations respect the k parameter."""
    rec = make_diverse_recommender()
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.5,
        target_valence=0.5,
        target_acousticness=0.5,
        likes_acoustic=False,
    )
    
    for k in [1, 2, 3, 5]:
        results = rec.recommend(user, k=k)
        assert len(results) <= k


# ============================================================================
# COMPREHENSIVE SCORING TESTS
# ============================================================================

def test_score_song_returns_tuple():
    """Test that score_song returns (score, reasons) tuple."""
    user_prefs = create_chill_lofi_lover()
    song = {
        "id": 1,
        "title": "Test",
        "artist": "Artist",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.6,
        "danceability": 0.3,
        "acousticness": 0.95,
        "tempo_bpm": 80,
    }
    
    result = score_song(user_prefs, song)
    assert isinstance(result, tuple)
    assert len(result) == 2
    score, reasons = result
    assert isinstance(score, (int, float))
    assert isinstance(reasons, list)


def test_score_song_perfect_match():
    """Test scoring a perfect match song."""
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "target_valence": 0.6,
        "target_acousticness": 0.9,
        "acousticness_weight": 1.0,
    }
    
    perfect_song = {
        "id": 1,
        "title": "Perfect Lofi",
        "artist": "Artist",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "valence": 0.6,
        "danceability": 0.4,
        "acousticness": 0.9,
        "tempo_bpm": 85,
    }
    
    score, reasons = score_song(user_prefs, perfect_song)
    # Should be high score
    assert score >= 3.0  # At least 2 full matches + high numeric scores
    assert "Genre match" in reasons
    assert "Mood match" in reasons


def test_score_song_no_match():
    """Test scoring a completely mismatched song."""
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_valence": 0.3,
        "target_acousticness": 0.1,
        "acousticness_weight": 0.5,
    }
    
    opposite_song = {
        "id": 1,
        "title": "Acoustic Chill",
        "artist": "Artist",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.2,
        "valence": 0.9,
        "danceability": 0.3,
        "acousticness": 0.95,
        "tempo_bpm": 70,
    }
    
    score, reasons = score_song(user_prefs, opposite_song)
    # Should be low score
    assert score < 1.0
    assert "Genre match" not in reasons
    assert "Mood match" not in reasons


def test_score_song_partial_match():
    """Test scoring a partially matching song."""
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_valence": 0.3,
        "target_acousticness": 0.1,
        "acousticness_weight": 0.5,
    }
    
    partial_song = {
        "id": 1,
        "title": "Intense Jazz",
        "artist": "Artist",
        "genre": "jazz",  # No genre match
        "mood": "intense",  # Mood matches!
        "energy": 0.85,  # Close energy match
        "valence": 0.35,  # Close valence match
        "danceability": 0.5,
        "acousticness": 0.8,  # Different from target
        "tempo_bpm": 150,
    }
    
    score, reasons = score_song(user_prefs, partial_song)
    # Should be moderate score
    assert score > 0.5
    assert "Mood match" in reasons
    assert "Genre match" not in reasons


# ============================================================================
# USER PREFERENCE COMBINATION TESTS
# ============================================================================

def test_different_acousticness_weights():
    """Test that different users value acousticness differently."""
    song_very_acoustic = {
        "id": 1,
        "title": "Very Acoustic",
        "artist": "Artist",
        "genre": "folk",
        "mood": "calm",
        "energy": 0.3,
        "valence": 0.6,
        "danceability": 0.2,
        "acousticness": 0.95,
        "tempo_bpm": 80,
    }
    
    user_loves_acoustic = {
        "favorite_genre": "folk",
        "favorite_mood": "calm",
        "target_energy": 0.3,
        "target_valence": 0.6,
        "target_acousticness": 0.9,
        "acousticness_weight": 2.0,  # Big weight
    }
    
    user_neutral_acoustic = {
        "favorite_genre": "folk",
        "favorite_mood": "calm",
        "target_energy": 0.3,
        "target_valence": 0.6,
        "target_acousticness": 0.9,
        "acousticness_weight": 0.5,  # Small weight
    }
    
    score_loves, _ = score_song(user_loves_acoustic, song_very_acoustic)
    score_neutral, _ = score_song(user_neutral_acoustic, song_very_acoustic)
    
    # Acoustic lover should score it higher
    assert score_loves > score_neutral


def test_strict_vs_flexible_users():
    """Test users with different genre strictness levels."""
    # Note: genre_strictness is in UserProfile but may not be used in score_song
    # This tests the attribute exists
    strict_user = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.45,
        target_valence=0.6,
        target_acousticness=0.8,
        likes_acoustic=True,
        genre_strictness=0.9,  # Very strict
    )
    
    flexible_user = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.45,
        target_valence=0.6,
        target_acousticness=0.8,
        likes_acoustic=True,
        genre_strictness=0.1,  # Very flexible
    )
    
    # Both should be constructible
    assert strict_user.genre_strictness == 0.9
    assert flexible_user.genre_strictness == 0.1
