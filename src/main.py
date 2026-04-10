"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Define test profiles
    test_profiles = [
        # Standard Profiles
        {"name": "High-Energy Pop", "genre": "pop", "mood": "happy", "energy": 0.9},
        {"name": "Chill Lofi", "genre": "lofi", "mood": "chill", "energy": 0.3},
        {"name": "Deep Intense Rock", "genre": "rock", "mood": "intense", "energy": 0.95},
        
        # Adversarial / Edge Cases
        {"name": "Angry Lofi (Mismatched Mood)", "genre": "lofi", "mood": "angry", "energy": 0.1},
        {"name": "High-Energy Classical (Mismatched Energy)", "genre": "classical", "mood": "energetic", "energy": 0.9},
        {"name": "Conflicting Mood/Energy", "mood": "sad", "energy": 0.9}
    ]

    for profile in test_profiles:
        profile_name = profile.pop("name", "Unnamed Profile")
        print("\n" + "="*50)
        print(f" 👤 PROFILE: {profile_name}")
        print(f"    Prefs: {profile}")
        print("="*50)

        recommendations = recommend_songs(profile, songs, k=5)

        print("\n 🎵 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{i}. {song['title'].upper()} by {song['artist']}")
            print(f"   🏆 Final Score: {score:.2f}")
            print("   ✨ Why you'll love it:")
            
            reasons = explanation.split("; ")
            for reason in reasons:
                print(f"      • {reason}")
            print("-" * 30)

if __name__ == "__main__":
    main()
