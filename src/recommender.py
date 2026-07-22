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

def _score_song_attributes(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """Shared Algorithm Recipe used by both the OOP and functional recommenders."""
    score = 0.0
    reasons: List[str] = []

    if genre == favorite_genre:
        score += 2.0
        reasons.append(f"genre match: {genre} (+2.0)")

    if mood == favorite_mood:
        score += 1.0
        reasons.append(f"mood match: {mood} (+1.0)")

    energy_gap = abs(energy - target_energy)
    energy_points = round(2.0 * (1 - energy_gap), 2)
    score += energy_points
    reasons.append(f"energy similarity: target {target_energy}, song {energy} (+{energy_points:.2f})")

    if likes_acoustic and acousticness >= 0.5:
        score += 1.0
        reasons.append(f"acoustic preference match: acousticness {acousticness} (+1.0)")
    elif not likes_acoustic and acousticness < 0.5:
        score += 1.0
        reasons.append(f"acoustic preference match: acousticness {acousticness} (+1.0)")

    return round(score, 2), reasons

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores one Song against a UserProfile using the shared Algorithm Recipe."""
        return _score_song_attributes(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Ranks all songs for a user and returns the top k Song objects."""
        scored = [(song, *self._score(user, song)) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _score, _reasons in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains, in one sentence, why a song scored the way it did for a user."""
        score, reasons = self._score(user, song)
        if not reasons:
            return f"No strong matches found (score: {score:.2f})."
        return f"Score {score:.2f} because " + "; ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song dict against a user_prefs dict using the shared Algorithm Recipe."""
    return _score_song_attributes(
        song["genre"],
        song["mood"],
        song["energy"],
        song["acousticness"],
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        user_prefs.get("energy", 0.0),
        user_prefs.get("likes_acoustic", False),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, then returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
