"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from textwrap import shorten

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

from .recommender import (
    get_available_scoring_modes,
    get_mode_max_score,
    load_songs,
    recommend_songs,
)


def _build_ascii_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(str(cell)))

    def fmt_row(row: list[str]) -> str:
        return "| " + " | ".join(str(cell).ljust(widths[idx]) for idx, cell in enumerate(row)) + " |"

    separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    lines = [separator, fmt_row(headers), separator]
    lines.extend(fmt_row(row) for row in rows)
    lines.append(separator)
    return "\n".join(lines)


def _format_recommendation_table(recommendations: list, max_score: float) -> str:
    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    rows = []
    for idx, (song, score, explanation) in enumerate(recommendations, 1):
        rows.append(
            [
                str(idx),
                song["title"],
                song["artist"],
                f"{score:.2f}/{max_score:.2f}",
                shorten(explanation, width=88, placeholder="..."),
            ]
        )

    if tabulate is not None:
        return tabulate(rows, headers=headers, tablefmt="fancy_grid")

    return _build_ascii_table(headers, rows)


def run_profile(
    profile_name: str,
    user_prefs: dict,
    songs: list,
    k: int = 5,
    scoring_mode: str = "balanced",
) -> None:
    """Run and print recommendations for a single user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k, scoring_mode=scoring_mode)
    max_score = get_mode_max_score(scoring_mode)

    print("\n" + "=" * 70)
    print(f"PROFILE: {profile_name}")
    print("=" * 70)
    print(f"Mode={scoring_mode}")
    print("-" * 70)
    print(f"Genre={user_prefs['genre']}, Mood={user_prefs['mood']}, Energy={user_prefs['energy']}, Acoustic={user_prefs.get('likes_acoustic', False)}")
    print("=" * 70 + "\n")

    if not recommendations:
        print("No recommendations found.")
        return

    print(_format_recommendation_table(recommendations, max_score))
    print()

    print(f"Total recommendations: {len(recommendations)}")
    print("=" * 70 + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Switch this value to try different ranking strategies.
    active_scoring_mode = "genre_first"
    print(f"Available modes: {', '.join(get_available_scoring_modes())}")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.3,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "likes_acoustic": False,
        },
        # --- Adversarial / Edge Case Profiles ---
        "High-Energy Sad (mood never exists)": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Genre Ghost - Classical (genre absent)": {
            "genre": "classical",
            "mood": "relaxed",
            "energy": 0.4,
            "likes_acoustic": True,
        },
        "Conflicted Acoustic Rocker": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "likes_acoustic": True,
        },
        "Mid-Energy Ambiguous (energy=0.5)": {
            "genre": "synthwave",
            "mood": "moody",
            "energy": 0.5,
            "likes_acoustic": False,
        },
        "Perfect Mismatch (no genre or mood in catalog)": {
            "genre": "country",
            "mood": "angry",
            "energy": 0.6,
            "likes_acoustic": False,
        },
    }

    for profile_name, user_prefs in profiles.items():
        run_profile(profile_name, user_prefs, songs, k=5, scoring_mode=active_scoring_mode)


if __name__ == "__main__":
    main()
