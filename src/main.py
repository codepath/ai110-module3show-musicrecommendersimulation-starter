
"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "genre": "disco",
        "mood": "celebratory",
        "energy": 0.85,
        "tempo_bpm": 120,
        "valence": 0.9,
        "danceability": 0.95,
        "acousticness": 0.2
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for song, score, explanation in recommendations:
        print(f"{song['title']:<25} | Score: {score:>5.2f}")
        print("  Reasons:")
        for reason in explanation.split(';'):
            print(f"    - {reason.strip()}")
        print("-" * 40)


if __name__ == "__main__":
    main()
