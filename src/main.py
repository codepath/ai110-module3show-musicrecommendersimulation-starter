"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "acousticness": 0.2,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 64
    print("\n" + "=" * width)
    print(f"TOP {len(recommendations)} RECOMMENDATIONS")
    print(
        f"Profile: {user_prefs['genre']} / {user_prefs['mood']} | "
        f"energy {user_prefs['energy']} | valence {user_prefs['valence']} | "
        f"acoustic {user_prefs['acousticness']}"
    )
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00   [{song['genre']}, {song['mood']}]")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print("\n" + "=" * width)


if __name__ == "__main__":
    main()
