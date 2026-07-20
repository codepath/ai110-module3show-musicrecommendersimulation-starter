import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    """Load songs from a CSV file with numeric fields converted to numbers."""
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and explain the result."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 1.5
        reasons.append("genre match (+1.5)")

    if song["mood"] == user_prefs["mood"]:
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_similarity = max(0.0, 1 - abs(song["energy"] - user_prefs["energy"]))
    energy_points = 4.0 * energy_similarity
    score += energy_points
    reasons.append(f"energy close to target (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        acoustic_match = (
            song["acousticness"] >= 0.5
            if user_prefs["likes_acoustic"]
            else song["acousticness"] < 0.5
        )
        if acoustic_match:
            score += 1.0
            reasons.append("acousticness matches preference (+1.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked by their preference scores."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    ranked_songs = sorted(scored_songs, key=lambda recommendation: recommendation[1], reverse=True)
    return ranked_songs[:k]
