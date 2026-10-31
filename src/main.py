"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    divider = "-" * 60
    acoustic = "likes acoustic" if user_prefs.get("likes_acoustic") else "prefers non-acoustic"

    print("\n" + "=" * 60)
    print("TOP RECOMMENDATIONS")
    print(
        f"Profile: {user_prefs['genre']} | {user_prefs['mood']} | "
        f"energy {user_prefs['energy']:.2f} | {acoustic}"
    )
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f} / 1.00")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     * {reason}")
        print(divider)


if __name__ == "__main__":
    main()
