"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

from src.recommender import (
    DEFAULT_STRATEGY, STRATEGIES, load_songs, max_score, recommend_songs,
)


WIDTH = 64

def print_recommendations(
    user_prefs: dict, recommendations: list, strategy=DEFAULT_STRATEGY, show_mode: bool = False
) -> None:
    """Prints the ranked recommendations as a readable terminal layout."""
    print("=" * WIDTH)
    print("MUSIC RECOMMENDER".center(WIDTH))
    print("=" * WIDTH)
    print(
        f"Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}"
    )
    extras = {k: v for k, v in user_prefs.items() if k not in ("genre", "mood", "energy")}
    if extras:
        print("Advanced: " + ", ".join(f"{k}={v}" for k, v in extras.items()))
    if show_mode:
        print(f"Mode: {strategy.name} - {strategy.description}")
    top_score = max_score(user_prefs, strategy)
    print(f"Top {len(recommendations)} recommendations")
    print("-" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  by {song['artist']}")
        print(f"    Score: {score:.2f} / {top_score:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print("\n" + "=" * WIDTH)


# Distinct taste profiles used to compare recommender behavior
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    # Adversarial / edge-case profiles
    "Conflicting: Sad but High Energy": {"genre": "pop", "mood": "sad", "energy": 0.9},
    "Genre-Only Trap (Metal, Chill, Low)": {"genre": "metal", "mood": "chill", "energy": 0.2},
    "Classical + Angry + Max Energy": {"genre": "classical", "mood": "angry", "energy": 1.0},
    "Out-of-Range Energy (2.0)": {"genre": "lofi", "mood": "chill", "energy": 2.0},
    "Case Mismatch (Pop/Happy)": {"genre": "Pop", "mood": "Happy", "energy": 0.8},
    "Unknown Genre and Mood": {"genre": "k-pop", "mood": "sad", "energy": 0.5},
    # Advanced-feature profiles (use popularity, decade, mood tags, language, instrumentalness)
    "Nostalgic 90s Listener": {
        "genre": "country", "mood": "nostalgic", "energy": 0.5,
        "decade": 1990, "mood_tags": ["nostalgic", "warm", "wistful"], "popularity": 50,
    },
    "Mainstream Hit Seeker": {
        "genre": "pop", "mood": "happy", "energy": 0.85,
        "popularity": 95, "decade": 2020, "mood_tags": ["uplifting", "energetic"],
    },
    "Spanish-Language Night Out": {
        "genre": "latin", "mood": "passionate", "energy": 0.85,
        "language": "spanish", "mood_tags": ["passionate", "romantic"], "popularity": 80,
    },
    "Instrumental Study Session": {
        "genre": "lofi", "mood": "focused", "energy": 0.4,
        "language": "instrumental", "instrumentalness": 0.9,
        "mood_tags": ["focused", "calm", "steady"], "popularity": 30,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--mode",
        choices=[*STRATEGIES, "all"],
        help=f"ranking mode (default: {DEFAULT_STRATEGY.key}); 'all' runs every mode",
    )
    parser.add_argument(
        "--profile",
        help="run only profiles whose name contains this text (e.g. rock)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    songs = load_songs("data/songs.csv")

    if args.mode == "all":
        strategies = list(STRATEGIES.values())
    else:
        strategies = [STRATEGIES[args.mode] if args.mode else DEFAULT_STRATEGY]

    profiles = {
        name: prefs for name, prefs in PROFILES.items()
        if not args.profile or args.profile.lower() in name.lower()
    }
    if not profiles:
        raise SystemExit(f"No profile name contains '{args.profile}'.")

    for name, user_prefs in profiles.items():
        for strategy in strategies:
            print(f"\n>>> {name}")
            recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)
            print_recommendations(
                user_prefs, recommendations, strategy, show_mode=args.mode is not None
            )


if __name__ == "__main__":
    main()
