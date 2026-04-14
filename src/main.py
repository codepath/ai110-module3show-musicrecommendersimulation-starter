"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict
from recommender import (
    load_songs, 
    recommend_songs,
    create_chill_lofi_lover,
    create_intense_rock_fan,
    create_jazz_soul_lover
)


# =============================================================================
# ADVERSARIAL / EDGE CASE USER PROFILES
# =============================================================================

def create_conflicting_preferences_user() -> Dict:
    """
    EDGE CASE: User with conflicting preferences.
    High energy but sad mood - these typically contradict each other.
    Expected: Algorithm should struggle to find good matches.
    """
    return {
        "favorite_genre": "rock",
        "favorite_mood": "sad",  # Sad mood typically goes with low energy
        "target_energy": 0.90,    # But this user wants high energy!
        "target_valence": 0.20,   # Low valence (sad)
        "target_acousticness": 0.50,
        "acousticness_weight": 1.0,
        "likes_acoustic": False,
        "genre_strictness": 0.5
    }


def create_impossible_genre_user() -> Dict:
    """
    EDGE CASE: User looking for a non-existent genre.
    Will only score if energy/mood/etc. happen to match.
    Expected: No genre bonus, relies entirely on numeric attributes.
    """
    return {
        "favorite_genre": "dubstep",  # Not in the dataset
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "target_valence": 0.50,
        "target_acousticness": 0.10,
        "acousticness_weight": 0.8,
        "likes_acoustic": False,
        "genre_strictness": 0.8
    }


def create_acoustic_paradox_user() -> Dict:
    """
    EDGE CASE: User wants BOTH high acousticness AND high energy.
    Typically contradictory (acoustic = mellow, energy = intense).
    Expected: May produce odd combinations or lower scores.
    """
    return {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.95,        # Very high energy
        "target_valence": 0.70,
        "target_acousticness": 0.90,  # Very high acousticness
        "acousticness_weight": 1.5,   # Heavy weighting
        "likes_acoustic": True,
        "genre_strictness": 0.6
    }


def create_all_extremes_user() -> Dict:
    """
    EDGE CASE: User with extreme values on all dimensions.
    May struggle to find matches in a normal dataset.
    Expected: Probably low scores across the board.
    """
    return {
        "favorite_genre": "jazz",
        "favorite_mood": "focused",
        "target_energy": 0.05,         # Extremely low
        "target_valence": 0.95,        # Extremely high
        "target_acousticness": 0.99,   # Extremely high
        "acousticness_weight": 2.0,    # Extra weight
        "likes_acoustic": True,
        "genre_strictness": 0.95        # Very strict
    }


def create_all_neutral_user() -> Dict:
    """
    EDGE CASE: User with all neutral/average preferences.
    Which song wins when everything is equally moderate?
    Expected: Possibly random/unclear winner based on rounding.
    """
    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.50,
        "target_valence": 0.50,
        "target_acousticness": 0.50,
        "acousticness_weight": 1.0,
        "likes_acoustic": False,
        "genre_strictness": 0.5
    }


def create_inverted_preferences_user() -> Dict:
    """
    EDGE CASE: User wants rock music but with lofi/chill characteristics.
    Rock should be loud & acoustic/synth-heavy, but user wants low energy.
    Expected: May get rock songs with unusual scoring.
    """
    return {
        "favorite_genre": "rock",
        "favorite_mood": "chill",     # Unusual for rock!
        "target_energy": 0.25,        # Very low for rock
        "target_valence": 0.65,
        "target_acousticness": 0.85,  # High acousticness for rock
        "acousticness_weight": 1.3,
        "likes_acoustic": True,
        "genre_strictness": 0.4
    }


def main() -> None:
    print("=" * 70)
    print("[MUSIC RECOMMENDER SIMULATION]")
    print("=" * 70)
    
    songs = load_songs("data/songs.csv")
    
    # =======================================================================
    # STANDARD PROFILES
    # =======================================================================
    
    # PROFILE 1: Chill Lofi Lover
    print("\n\n[PROFILE 1] Chill Lofi Lover")
    print("-" * 70)
    user_prefs_1 = create_chill_lofi_lover()
    print(f"Preferences: {user_prefs_1}")
    
    recommendations_1 = recommend_songs(user_prefs_1, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_1:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()
    
    # PROFILE 2: Intense Rock Fan
    print("\n\n[PROFILE 2] Intense Rock Fan")
    print("-" * 70)
    user_prefs_2 = create_intense_rock_fan()
    print(f"Preferences: {user_prefs_2}")
    
    recommendations_2 = recommend_songs(user_prefs_2, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_2:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # PROFILE 3: Jazz/Soul Lover
    print("\n\n[PROFILE 3] Jazz/Soul Lover")
    print("-" * 70)
    user_prefs_3 = create_jazz_soul_lover()
    print(f"Preferences: {user_prefs_3}")
    
    recommendations_3 = recommend_songs(user_prefs_3, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_3:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # =======================================================================
    # ADVERSARIAL / EDGE CASE PROFILES
    # =======================================================================
    
    # ADVERSARIAL 1: Conflicting Preferences (High Energy + Sad Mood)
    print("\n\n[ADVERSARIAL 1] Conflicting Preferences: Sad but Energetic")
    print("-" * 70)
    print("Challenge: Can the recommender handle high energy + sad mood?")
    user_adv_1 = create_conflicting_preferences_user()
    print(f"Preferences: {user_adv_1}")
    
    recommendations_adv_1 = recommend_songs(user_adv_1, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_1:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # ADVERSARIAL 2: Impossible Genre
    print("\n\n[ADVERSARIAL 2] Impossible Genre: Dubstep (Not in Dataset)")
    print("-" * 70)
    print("Challenge: What happens when favorite_genre doesn't exist?")
    user_adv_2 = create_impossible_genre_user()
    print(f"Preferences: {user_adv_2}")
    
    recommendations_adv_2 = recommend_songs(user_adv_2, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_2:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # ADVERSARIAL 3: Acoustic Paradox (High Acousticness + High Energy)
    print("\n\n[ADVERSARIAL 3] Acoustic Paradox: Energetic Acoustic Music")
    print("-" * 70)
    print("Challenge: Typically contradictory attributes (acoustic=mellow, energy=intense)")
    user_adv_3 = create_acoustic_paradox_user()
    print(f"Preferences: {user_adv_3}")
    
    recommendations_adv_3 = recommend_songs(user_adv_3, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_3:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # ADVERSARIAL 4: All Extreme Values
    print("\n\n[ADVERSARIAL 4] All Extremes: Very Low Energy + Very High Values")
    print("-" * 70)
    print("Challenge: Can algorithm find matches with extreme, conflicting values?")
    user_adv_4 = create_all_extremes_user()
    print(f"Preferences: {user_adv_4}")
    
    recommendations_adv_4 = recommend_songs(user_adv_4, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_4:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # ADVERSARIAL 5: All Neutral Values
    print("\n\n[ADVERSARIAL 5] All Neutral: Everything at 0.5 (Average)")
    print("-" * 70)
    print("Challenge: All songs equally good/bad? Which wins on tie-breaks?")
    user_adv_5 = create_all_neutral_user()
    print(f"Preferences: {user_adv_5}")
    
    recommendations_adv_5 = recommend_songs(user_adv_5, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_5:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()

    # ADVERSARIAL 6: Inverted Preferences
    print("\n\n[ADVERSARIAL 6] Inverted: Rock Music but with Lofi Characteristics")
    print("-" * 70)
    print("Challenge: Rock + Chill is unusual. Will the algorithm find good matches?")
    user_adv_6 = create_inverted_preferences_user()
    print(f"Preferences: {user_adv_6}")
    
    recommendations_adv_6 = recommend_songs(user_adv_6, songs, k=5)
    
    print("\nTop 5 recommendations:\n")
    for rec in recommendations_adv_6:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Explanation: {explanation}")
        print()


if __name__ == "__main__":
    main()
