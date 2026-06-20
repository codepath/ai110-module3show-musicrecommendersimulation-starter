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
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs against a UserProfile and return the top k Song objects."""
        def score(song: Song) -> float:
            s = 0.0
            if song.genre == user.favorite_genre:
                s += 0.40
            if song.mood == user.favorite_mood:
                s += 0.35
            s += 0.25 * (1.0 - abs(song.energy - user.target_energy))
            return s

        return sorted(self.songs, key=score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.2:
            reasons.append(f"energy close to your target ({song.energy})")
        if not reasons:
            return "Closest available match based on energy."
        return "Recommended because: " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of song dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences using weighted genre, mood, and energy matching; returns (score, reasons)."""
    score = 0.0
    reasons = []

    # genre match — weight 0.40
    if song["genre"] == user_prefs["genre"]:
        score += 0.40
        reasons.append(f"genre match: {song['genre']} (+0.40)")

    # mood match — weight 0.35
    if song["mood"] == user_prefs["mood"]:
        score += 0.35
        reasons.append(f"mood match: {song['mood']} (+0.35)")

    # energy closeness — weight 0.25
    energy_closeness = 1.0 - abs(song["energy"] - user_prefs["energy"])
    energy_contribution = round(0.25 * energy_closeness, 2)
    score += energy_contribution
    reasons.append(f"energy closeness: {song['energy']} vs {user_prefs['energy']} (+{energy_contribution})")

    return round(score, 3), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user preferences and return the top k ranked by score with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
