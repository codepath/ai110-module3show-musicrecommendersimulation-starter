"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # When run as a package: `python -m src.main`
    from .recommender import load_songs, recommend_songs
except ImportError:
    # When run from inside src/: `python main.py`
    from recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print recommendations in a clean, readable terminal layout."""
    line = "=" * 60

    # Header: show what taste profile we recommended for.
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print(f"\n{line}")
    print(f"  Top {len(recommendations)} recommendations for: {profile}")
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:.2f}")
        print("     Reasons:")
        # `explanation` is the reasons joined by "; " — split back into bullets.
        for reason in explanation.split("; "):
            print(f"       • {reason}")

    print(f"\n{line}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
