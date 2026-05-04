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
    """Load songs from a CSV file and return as a list of dicts with numeric fields converted to float/int."""

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using mood, genre, energy, valence, and danceability."""

    score = 0.0
    reasons = []

    if song.get("mood") == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match (+2.0)")

    if song.get("genre") == user_prefs.get("genre"):
        score += 1.5
        reasons.append("genre match (+1.5)")

    if "energy" in user_prefs and "energy" in song:
        energy_score = 1.5 * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score:.2f})")

    if "valence" in user_prefs and "valence" in song:
        valence_score = 1.0 * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += valence_score
        reasons.append(f"valence proximity (+{valence_score:.2f})")

    if "danceability" in user_prefs and "danceability" in song:
        dance_score = 0.5 * (1 - abs(song["danceability"] - user_prefs["danceability"]))
        score += dance_score
        reasons.append(f"danceability proximity (+{dance_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank by score descending, and return the top k results with explanations."""

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]


