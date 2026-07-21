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

NUMERIC_FIELDS_FLOAT = ("energy", "valence", "danceability", "acousticness")
NUMERIC_FIELDS_INT = ("id", "tempo_bpm")

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in NUMERIC_FIELDS_INT:
                row[field] = int(row[field])
            for field in NUMERIC_FIELDS_FLOAT:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using the Algorithm Recipe, returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if user_prefs.get("genre") == song["genre"]:
        score += 3
        reasons.append(f"matches favorite genre '{song['genre']}'")

    if user_prefs.get("mood") == song["mood"]:
        score += 2
        reasons.append(f"matches favorite mood '{song['mood']}'")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = 2 * (1 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} close to target {target_energy:.2f}"
        )

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is True and song["acousticness"] > 0.6:
        score += 1
        reasons.append("acoustic sound matches your preference")
    elif likes_acoustic is False and song["acousticness"] < 0.4:
        score += 1
        reasons.append("produced sound matches your preference")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song against user_prefs and return the top k, ranked highest score first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda entry: entry[1], reverse=True)
    return [
        (song, score, ", ".join(reasons))
        for song, score, reasons in scored[:k]
    ]
