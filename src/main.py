"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

WIDTH = 64

# Typical listeners
STANDARD_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy",
        "energy": 0.9, "valence": 0.85, "acousticness": 0.1,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill",
        "energy": 0.4, "valence": 0.6, "acousticness": 0.8,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense",
        "energy": 0.92, "valence": 0.45, "acousticness": 0.08,
    },
}

# Edge cases designed to trick the scoring logic
ADVERSARIAL_PROFILES = {
    "Conflicting: Sad but Energetic": {
        "genre": "classical", "mood": "melancholy",
        "energy": 0.9, "valence": 0.1, "acousticness": 0.95,
    },
    "Unknown Genre and Mood": {
        "genre": "bossa nova", "mood": "dreamy",
        "energy": 0.5, "valence": 0.5, "acousticness": 0.5,
    },
    "Extreme Targets": {
        "genre": "metal", "mood": "peaceful",
        "energy": 0.0, "valence": 1.0, "acousticness": 0.0,
    },
}


# Profiles that use the advanced song features
ADVANCED_PROFILES = {
    "Mainstream Hits": {
        "genre": "pop", "mood": "happy",
        "energy": 0.85, "valence": 0.8, "acousticness": 0.15,
        "popularity": 90, "decade": 2020, "mood_tags": ["upbeat", "bright"],
    },
    "Nostalgic Throwback": {
        "genre": "country", "mood": "nostalgic",
        "energy": 0.5, "valence": 0.65, "acousticness": 0.7,
        "popularity": 55, "decade": 2000, "mood_tags": ["nostalgic", "warm"],
    },
    "Instrumental Study Session": {
        "genre": "lofi", "mood": "focused",
        "energy": 0.4, "valence": 0.6, "acousticness": 0.8,
        "instrumentalness": 0.9, "mood_tags": ["study", "cozy"], "avoid_explicit": True,
    },
    "Clean Workout": {
        "genre": "rock", "mood": "intense",
        "energy": 0.95, "valence": 0.5, "acousticness": 0.05,
        "mood_tags": ["workout", "powerful"], "avoid_explicit": True,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one profile in a readable layout."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * WIDTH)
    print(f"PROFILE: {name}")
    print(
        f"{user_prefs['genre']} / {user_prefs['mood']} | "
        f"energy {user_prefs['energy']} | valence {user_prefs['valence']} | "
        f"acoustic {user_prefs['acousticness']}"
    )
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00   [{song['genre']}, {song['mood']}]")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print("\n" + "=" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    all_profiles = {**STANDARD_PROFILES, **ADVERSARIAL_PROFILES, **ADVANCED_PROFILES}
    for name, prefs in all_profiles.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
