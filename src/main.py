"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

# Everyday user preference profiles.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
}

# Adversarial / edge-case profiles from the System Evaluation pass — each is designed
# to probe a specific way the scoring logic could be "tricked" or behave oddly.
ADVERSARIAL_PROFILES = {
    # High target_energy paired with a "sad" mood that doesn't exactly match any
    # catalog mood string (closest is "melancholic") - tests conflicting signals
    # plus exact-string mood mismatch.
    "Conflicting Signals (Energetic + Sad)": {"genre": "blues", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    # No song in the catalog has genre "country" - tests graceful fallback to
    # mood/energy/acoustic scoring instead of crashing or returning nothing.
    "Genre Not In Catalog": {"genre": "country", "mood": "happy", "energy": 0.5, "likes_acoustic": False},
    # target_energy is outside the 0-1 scale every song uses - tests whether the
    # energy-closeness formula degrades gracefully (can go negative) rather than erroring.
    "Out-of-Range Energy": {"genre": "edm", "mood": "triumphant", "energy": 1.5, "likes_acoustic": False},
    # EDM is definitionally non-acoustic, but the user claims to like acoustic songs -
    # tests whether genre match and acoustic mismatch pull the ranking in opposite directions.
    "Contradictory Acoustic Preference": {"genre": "edm", "mood": "triumphant", "energy": 0.9, "likes_acoustic": True},
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    header = f"{name} (genre={user_prefs.get('genre')}, mood={user_prefs.get('mood')}, energy={user_prefs.get('energy')})"
    print(f"\n{header}")
    print("=" * len(header))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)

    print("\n\n--- System Evaluation: Adversarial / Edge Case Profiles ---")
    for name, user_prefs in ADVERSARIAL_PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
