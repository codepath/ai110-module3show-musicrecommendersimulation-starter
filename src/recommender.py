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

# Algorithm Recipe weights (see README "Algorithm Recipe"). A Weight Shift
# sensitivity experiment (genre=1.0, energy=2.0) was tested and reverted -
# see README "Experiments You Tried" for the results.
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

def _score_components(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """Scores one song's raw attributes against a user's raw preferences using the Algorithm Recipe."""
    score = 0.0
    reasons = []

    if genre == favorite_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({genre}) (+{GENRE_WEIGHT:.1f})")

    if mood == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({mood}) (+{MOOD_WEIGHT:.1f})")

    energy_points = ENERGY_WEIGHT * (1 - abs(energy - target_energy))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    if likes_acoustic and acousticness > 0.6:
        score += ACOUSTIC_WEIGHT
        reasons.append(f"acoustic preference match (+{ACOUSTIC_WEIGHT:.1f})")
    elif not likes_acoustic and acousticness < 0.4:
        score += ACOUSTIC_WEIGHT
        reasons.append(f"non-acoustic preference match (+{ACOUSTIC_WEIGHT:.1f})")

    return score, reasons

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user profile and returns the top k, highest-scoring first."""
        scored = [
            (song, _score_components(
                song.genre, song.mood, song.energy, song.acousticness,
                user.favorite_genre, user.favorite_mood, user.target_energy, user.likes_acoustic,
            )[0])
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable, semicolon-joined list of reasons a song scored the way it did."""
        _, reasons = _score_components(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood, user.target_energy, user.likes_acoustic,
        )
        return "; ".join(reasons) if reasons else "No matching attributes."

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    numeric_int_fields = {"id"}
    numeric_float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_int_fields:
                row[field] = int(row[field])
            for field in numeric_float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song dict against a user_prefs dict, returning (score, reasons)."""
    return _score_components(
        song["genre"], song["mood"], song["energy"], song["acousticness"],
        user_prefs.get("genre"), user_prefs.get("mood"), user_prefs.get("energy", 0.5),
        user_prefs.get("likes_acoustic", False),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song against user_prefs and returns the top k as (song, score, explanation) tuples."""
    def judge(song: Dict) -> Tuple[Dict, float, str]:
        """Scores one song and packages it with its explanation string."""
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No matching attributes."
        return song, score, explanation

    scored = [judge(song) for song in songs]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
