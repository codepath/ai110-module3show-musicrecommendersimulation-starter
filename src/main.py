"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def run_profile(label: str, user_prefs: dict, songs: list) -> None:
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"{'=' * 50}")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("-" * 50)
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"#{i} {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.5")
        print(f"    Why   : {explanation}")
        print("-" * 50)


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        ("High-Energy Pop", {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "valence": 0.80,
            "danceability": 0.85,
        }),
        ("Chill Lofi", {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.40,
            "valence": 0.60,
            "danceability": 0.62,
        }),
        ("Deep Intense Rock", {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.91,
            "valence": 0.40,
            "danceability": 0.65,
        }),
        ("Adversarial - High Energy but Sad", {
            "genre": "indie folk",
            "mood": "sad",
            "energy": 0.90,
            "valence": 0.25,
            "danceability": 0.80,
        }),
    ]

    for label, prefs in profiles:
        run_profile(label, prefs, songs)


if __name__ == "__main__":
    main()