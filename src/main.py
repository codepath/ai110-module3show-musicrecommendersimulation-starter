
"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""


from .recommender import load_songs, recommend_songs
from .adversarial_profiles import adversarial_profiles


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # User preference profiles
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "tempo_bpm": 128,
            "valence": 0.85,
            "danceability": 0.9,
            "acousticness": 0.1
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "tempo_bpm": 75,
            "valence": 0.6,
            "danceability": 0.6,
            "acousticness": 0.8
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 150,
            "valence": 0.5,
            "danceability": 0.7,
            "acousticness": 0.15
        }
    }


    # Run for normal profiles
    for profile_name, user_prefs in user_profiles.items():
        print(f"\n=== Recommendations for {profile_name} ===")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for song, score, explanation in recommendations:
            print(f"{song['title']:<25} | Score: {score:>5.2f}")
            print("  Reasons:")
            for reason in explanation.split(';'):
                print(f"    - {reason.strip()}")
            print("-" * 40)

    # Run for adversarial/edge case profiles
    for profile_name, user_prefs in adversarial_profiles.items():
        print(f"\n=== Recommendations for {profile_name} (Adversarial) ===")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for song, score, explanation in recommendations:
            print(f"{song['title']:<25} | Score: {score:>5.2f}")
            print("  Reasons:")
            for reason in explanation.split(';'):
                print(f"    - {reason.strip()}")
            print("-" * 40)


if __name__ == "__main__":
    main()
