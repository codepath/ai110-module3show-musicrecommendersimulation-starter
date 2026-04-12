# Adversarial/Edge Case User Profiles for Music Recommender
# These profiles are designed to test the scoring logic for unexpected or conflicting preferences.

adversarial_profiles = {
    # Conflicting: High energy but sad mood
    "High-Energy Sad": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "tempo_bpm": 130,
        "valence": 0.2,
        "danceability": 0.9,
        "acousticness": 0.1
    },
    # Impossible: Likes both high and low acousticness
    "Acoustic Paradox": {
        "genre": "folk",
        "mood": "peaceful",
        "energy": 0.5,
        "tempo_bpm": 90,
        "valence": 0.7,
        "danceability": 0.5,
        "acousticness": 0.0  # But expects high acousticness in folk
    },
    # Extreme: All maxed out
    "Everything Max": {
        "genre": "metal",
        "mood": "angry",
        "energy": 1.0,
        "tempo_bpm": 200,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0
    },
    # Extreme: All zero
    "Everything Min": {
        "genre": "classical",
        "mood": "reflective",
        "energy": 0.0,
        "tempo_bpm": 0,
        "valence": 0.0,
        "danceability": 0.0,
        "acousticness": 0.0
    },
    # Contradictory: Happy mood, but all other features are low
    "Happy But Low": {
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.1,
        "tempo_bpm": 60,
        "valence": 0.1,
        "danceability": 0.1,
        "acousticness": 0.9
    }
}
