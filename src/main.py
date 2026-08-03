"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender against a set of
user preference profiles -- including deliberately "adversarial" edge-case
profiles designed to probe whether the scoring logic can be tricked or produce
surprising results.

The scoring logic lives in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

# Support both `python -m src.main` (package import) and `python src/main.py`
# / `cd src && python main.py` (direct import).
try:
    from src.recommender import load_songs, recommend_songs, score_ceiling
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, score_ceiling

# Path to the catalog, resolved relative to this file so the script works no
# matter which directory it is launched from.
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


# --- User preference profiles ----------------------------------------------
# Each profile is a plain dict passed straight to recommend_songs().
# Keys (all optional): "genre", "mood", "energy" (0-1), "likes_acoustic".

# Three distinct "normal" profiles that a real listener might have.
NORMAL_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
}

# Adversarial / edge-case profiles: crafted to stress the scoring logic and
# see whether it can be "tricked" or produces unexpected rankings.
ADVERSARIAL_PROFILES = {
    # Conflicting signals: wants maximum energy but a downbeat "sad" mood.
    # ("sad" is not even a label in the catalog, so mood falls back to
    # objective similarity.) Does energy dominate, or does the sad-leaning
    # fallback pull in mellow songs?
    "Contradictory: high energy + sad": {
        "genre": "rock",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    # Wants loud, produced EDM energy but claims to love the acoustic sound.
    # Energy and acousticness point in opposite directions in the catalog.
    "Contradictory: loud EDM + acoustic lover": {
        "genre": "EDM",
        "mood": "dark",
        "energy": 0.95,
        "likes_acoustic": True,
    },
    # Labels absent from the catalog but recognized synonyms: "k-pop" -> pop,
    # "euphoric" -> uplifting. Exercises the out-of-vocabulary resolution so
    # the request scores against a real centroid instead of collapsing to zero.
    "Synonym resolution: k-pop / euphoric": {
        "genre": "k-pop",
        "mood": "euphoric",
        "energy": 0.5,
        "likes_acoustic": False,
    },
    # A genre and mood with no exact label AND no synonym. These stay
    # unmatchable, so scoring rides entirely on energy/acoustic and the
    # explanation should say so honestly.
    "Truly unknown genre & mood": {
        "genre": "polka",
        "mood": "chaotic",
        "energy": 0.5,
        "likes_acoustic": False,
    },
    # An almost-empty profile: only energy is expressed. Tests what happens
    # when most scoring terms are absent.
    "Sparse: energy only": {
        "energy": 0.5,
    },
    # Every field left at a neutral / boundary value. With no genre or mood
    # and mid energy, does anything meaningfully differentiate the songs?
    "Neutral / boundary": {
        "genre": "",
        "mood": "",
        "energy": 0.5,
        "likes_acoustic": False,
    },
}


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Run the recommender for one profile and print its top-k results."""
    print("=" * 60)
    print(f"Profile: {name}")
    print(f"Preferences: {user_prefs}")
    print("-" * 60)

    # Normalize against only the terms that can actually score, so results are
    # comparable across profiles (display only -- ranking uses the raw score).
    ceiling = score_ceiling(user_prefs, songs)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        normalized = 10.0 * score / ceiling if ceiling else 0.0
        print(f"{rank}. {song['title']} by {song['artist']} "
              f"[{song['genre']}/{song['mood']}] - Score: {score:.2f} "
              f"({normalized:.1f}/10)")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}\n")

    print("########## NORMAL PROFILES ##########\n")
    for name, prefs in NORMAL_PROFILES.items():
        run_profile(name, prefs, songs)

    print("########## ADVERSARIAL / EDGE-CASE PROFILES ##########\n")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
