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

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 70)
    print("MUSIC RECOMMENDER - TOP RECOMMENDATIONS")
    print("=" * 70)
    print(f"Profile: Genre={user_prefs['genre']}, Mood={user_prefs['mood']}, Energy={user_prefs['energy']}")
    print("=" * 70 + "\n")

    if not recommendations:
        print("No recommendations found.")
        return

    for idx, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{idx}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f} / 6.0")
        print(f"   Why: {explanation}")
        print()

    print("=" * 70)
    print(f"Total recommendations: {len(recommendations)}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
