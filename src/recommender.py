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
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        scored_songs = []
        for song in self.songs:
            song_data = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_data)
            scored_songs.append((score, song))

        ranked_songs = sorted(scored_songs, key=lambda item: item[0], reverse=True)
        return [song for _, song in ranked_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_data = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_data)
        return "; ".join(reasons) if reasons else "No strong match found."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dictionaries."""
    print(f"Loading songs from {csv_path}...")
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_MATCH_POINTS = 1.0
MOOD_MATCH_POINTS = 1.5
ENERGY_MATCH_POINTS = 2.0
ACOUSTICNESS_MATCH_POINTS = 0.5

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against a user's preferences."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        energy_points = closeness * ENERGY_MATCH_POINTS
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    if user_prefs.get("likes_acoustic"):
        acoustic_points = song["acousticness"] * ACOUSTICNESS_MATCH_POINTS
        score += acoustic_points
        reasons.append(f"acoustic bonus (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by relevance to user preferences."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong match found."
        scored_songs.append((song, score, explanation))

    ranked_songs = sorted(scored_songs, key=lambda item: item[1], reverse=True)
    return ranked_songs[:k]
