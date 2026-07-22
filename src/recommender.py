from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns:
        (total_score, reasons) where reasons is a list of human-readable
        strings explaining each contribution to the score.
    """
    score = 0.0
    reasons = []

    # --- Genre match (categorical, exact match bonus) ---
    genre_points = 2.0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += genre_points
        reasons.append(f"genre match ({song['genre']}) (+{genre_points:.1f})")

    # --- Mood match (categorical, exact match bonus) ---
    mood_points = 1.5
    if song["mood"] == user_prefs["favorite_mood"]:
        score += mood_points
        reasons.append(f"mood match ({song['mood']}) (+{mood_points:.1f})")

    # --- Energy closeness (numeric, reward closer to target) ---
    energy_weight = 2.0
    energy_diff = abs(user_prefs["target_energy"] - song["energy"])
    energy_closeness = 1 - energy_diff          # 1.0 = perfect match, 0.0 = max distance
    energy_score = energy_closeness * energy_weight
    score += energy_score
    reasons.append(
        f"energy closeness ({song['energy']:.2f} vs target {user_prefs['target_energy']:.2f}) "
        f"(+{energy_score:.2f})"
    )

    # --- Acoustic preference (boolean flag) ---
    acoustic_points = 1.0
    if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.5:
        score += acoustic_points
        reasons.append(f"matches acoustic preference ({song['acousticness']:.2f}) (+{acoustic_points:.1f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    scored.sort(key=lambda entry: entry[1], reverse=True)

    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in scored[:k]
    ]

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs