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
MAX_SCORE = 4.0  # 2.0 genre + 1.0 mood + 1.0 energy


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints the ranked recommendations as a readable terminal layout."""
    print("=" * WIDTH)
    print("MUSIC RECOMMENDER".center(WIDTH))
    print("=" * WIDTH)
    print(
        f"Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}"
    )
    print(f"Top {len(recommendations)} recommendations")
    print("-" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  by {song['artist']}")
        print(f"    Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print("\n" + "=" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
