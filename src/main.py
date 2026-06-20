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


    users = {
        # --- core profiles ---
        "Jackie (lofi/chill)": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "acousticness": 0.75,
        },
        "Alex (pop/happy)": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "acousticness": 0.2,
        },
        "Sam (rock/intense)": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "acousticness": 0.1,
        },
        # --- edge case profiles ---
        "Jordan (conflicting: high-energy + sad)": {
            "genre": "folk",
            "mood": "sad",
            "energy": 0.9,
            "acousticness": 0.8,
        },
        "Riley (genre with no catalog match)": {
            "genre": "reggae",
            "mood": "happy",
            "energy": 0.6,
            "acousticness": 0.5,
        },
        "Payton (perfectly average everything)": {
            "genre": "indie pop",
            "mood": "moody",
            "energy": 0.5,
            "acousticness": 0.5,
        },
    }

    for user_name, user_prefs in users.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\n" + "=" * 50)
        print(f"  Recommendations for {user_name}")
        print("=" * 50)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{i}. {song['title']} by {song['artist']}")
            print(f"   Score : {score:.2f}")
            print(f"   Why   : {explanation}")


if __name__ == "__main__":
    main()
