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
        """Return top k songs ranked by match to user preferences."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song is recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    try:
        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
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
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def calculate_score(song: Dict, user_genre: str, user_mood: str, user_energy: float, user_acoustic: bool) -> float:
        """Calculate a single song's score based on user preferences."""
        score = 0.0
        
        # Genre match: +2.0
        if song["genre"].strip().lower() == user_genre.strip().lower():
            score += 2.0
        
        # Mood match: +1.0
        if song["mood"].strip().lower() == user_mood.strip().lower():
            score += 1.0
        
        # Energy similarity: +2.0 × (1 - |song_energy - user_energy|), clamped to [0, 2.0]
        energy_diff = abs(song["energy"] - user_energy)
        energy_similarity = max(0.0, min(1.0, 1.0 - energy_diff))
        score += 2.0 * energy_similarity
        
        # Acoustic preference: +1.0
        song_is_acoustic = song["acousticness"] >= 0.5
        if song_is_acoustic == user_acoustic:
            score += 1.0
        
        return score
    
    def explain_score(song: Dict, score: float, user_genre: str, user_mood: str, user_energy: float, user_acoustic: bool) -> str:
        """Generate a human-readable explanation for why a song scored well."""
        reasons = []
        
        if song["genre"].strip().lower() == user_genre.strip().lower():
            reasons.append(f"matches your genre ({song['genre']})")
        
        if song["mood"].strip().lower() == user_mood.strip().lower():
            reasons.append(f"matches your mood ({song['mood']})")
        
        energy_diff = abs(song["energy"] - user_energy)
        if energy_diff <= 0.15:
            reasons.append(f"energy is very close ({song['energy']:.2f})")
        elif energy_diff <= 0.35:
            reasons.append(f"energy is close ({song['energy']:.2f})")
        
        song_is_acoustic = song["acousticness"] >= 0.5
        if user_acoustic and song_is_acoustic:
            reasons.append("fits your acoustic preference")
        if not user_acoustic and not song_is_acoustic:
            reasons.append("fits your preference for produced sound")
        
        if not reasons:
            return "Overall similarity to your profile"
        
        return ", ".join(reasons)
    
    user_genre = str(user_prefs.get("genre", "")).strip()
    user_mood = str(user_prefs.get("mood", "")).strip()
    user_energy = float(user_prefs.get("energy", 0.5))
    user_acoustic = bool(user_prefs.get("likes_acoustic", False))
    
    scored_songs = []
    for song in songs:
        score = calculate_score(song, user_genre, user_mood, user_energy, user_acoustic)
        explanation = explain_score(song, score, user_genre, user_mood, user_energy, user_acoustic)
        scored_songs.append((song, score, explanation))
    
    ranked = sorted(scored_songs, key=lambda item: item[1], reverse=True)
    
    return ranked[:k]
