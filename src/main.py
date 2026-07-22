"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:  # pragma: no cover - supports running the file directly
    from recommender import load_songs, recommend_songs


def get_sample_user_profiles():
    """Return a few distinct user preference dictionaries for demo purposes."""
    return {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Conflicting Mood-Energy": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "No Match Fallback": {
            "genre": "country",
            "mood": "melancholic",
            "energy": 0.2,
            "likes_acoustic": False,
        },
        "Acoustic Bonus Trap": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.2,
            "likes_acoustic": True,
        },
    }


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    user_profiles = get_sample_user_profiles()

    for profile_name, user_prefs in user_profiles.items():
        print(f"\nProfile: {profile_name}")
        recommendations = recommend_songs(user_prefs, songs, k=3)
        for index, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            reasons = [reason.strip() for reason in explanation.split(";") if reason.strip()]

            print(f"{index}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"     • {reason}")
            print()

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [reason.strip() for reason in explanation.split(";") if reason.strip()]

        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
