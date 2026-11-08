"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from src.recommender import MAX_SCORE, load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: "Upbeat Pop Listener"
    # Categorical features are scored as exact matches;
    # numeric targets (0.0-1.0) reward songs that are CLOSE to the value.
    user_prefs = {
        "favorite_genre": "pop",        # categorical: genre match
        "favorite_mood": "happy",       # categorical: mood match
        "target_energy": 0.70,          # lively, but not all-out intense
        "target_valence": 0.80,         # bright, positive feel
        "target_danceability": 0.80,    # wants a groove
        "likes_acoustic": False,        # prefers produced/electronic sound
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations("Upbeat Pop Listener", user_prefs, recommendations)


WIDTH = 64
BAR_LENGTH = 20


def score_bar(score: float) -> str:
    """Draw a text bar showing how close a score is to the maximum."""
    filled = round(BAR_LENGTH * score / MAX_SCORE)
    return "█" * filled + "░" * (BAR_LENGTH - filled)


def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    """Print the profile and each (song, score, explanation) in a readable block."""
    # Drop the "favorite_"/"target_" prefixes so the profile fits on one line.
    prefs_line = " · ".join(
        f"{key.removeprefix('favorite_').removeprefix('target_')}={value}"
        for key, value in user_prefs.items()
    )

    print()
    print("═" * WIDTH)
    print(f" Top {len(recommendations)} for: {profile_name}")
    print(textwrap.fill(prefs_line, WIDTH, initial_indent=" ", subsequent_indent=" "))
    print("═" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f" #{rank}  {song['title']} — {song['artist']}")
        print(f"     {song['genre']} · {song['mood']}")
        print(f"     Score: {score:.2f} / {MAX_SCORE:.2f}  {score_bar(score)}")
        print("     Why:")
        for reason in explanation.split("; "):
            print(f"       • {reason}")
        print(" " + "─" * (WIDTH - 1))


if __name__ == "__main__":
    main()
