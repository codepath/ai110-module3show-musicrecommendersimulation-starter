"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(recommendations) -> None:
    """
    Pretty-prints song recommendations to the terminal.
    """
    print("\n" + "=" * 55)
    print("  TOP SONG RECOMMENDATIONS")
    print("=" * 55)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why:   {explanation}")

    print("\n" + "=" * 55 + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    # NOTE: keys must match what score_song() reads (favorite_genre,
    # favorite_mood, target_energy, likes_acoustic) — not raw feature names.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
