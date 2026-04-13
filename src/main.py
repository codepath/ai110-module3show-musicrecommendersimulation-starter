"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, recommendations) -> None:
    """Print a formatted block of recommendations for a given profile."""
    print(f"\n{'=' * 52}")
    print(f"  Profile: {profile_name}")
    print(f"{'=' * 52}")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  {i}. {song['title']}  by {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']:.2f}")
        print(f"     Score: {score:.2f}")
        print(f"     Why:   {explanation}")


def main() -> None:
    csv_path = os.path.join("data", "songs.csv")
    songs = load_songs(csv_path)
    print(f"Loaded {len(songs)} songs.")

    profiles = [
        (
            "High-Energy Pop Fan",
            {"genre": "pop", "mood": "happy", "energy": 0.85},
        ),
        (
            "Chill Lofi Listener",
            {"genre": "lofi", "mood": "chill", "energy": 0.38},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.92},
        ),
        (
            "Edge Case: High-Energy but Sad (conflicting preferences)",
            {"genre": "ambient", "mood": "sad", "energy": 0.90},
        ),
    ]

    for name, prefs in profiles:
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, recs)

    print(f"\n{'=' * 52}\n")


if __name__ == "__main__":
    main()
