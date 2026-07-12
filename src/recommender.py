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
        """Store the catalog of songs to recommend from."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short human-readable reason this song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries (one per song).

    Numeric columns are converted from the CSV's raw strings into numbers so they
    can be used in math later:
      - `id`         -> int
      - `tempo_bpm`  -> int (whole beats per minute)
      - all other numeric features (energy, valence, danceability, acousticness)
                     -> float

    Text columns (title, artist, genre, mood) are left as strings.
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs

# Scoring weights (tunable knobs — change these to run the README experiments).
GENRE_WEIGHT = 2.0   # points awarded for an exact genre match
MOOD_WEIGHT = 1.5    # points awarded for an exact mood match
ENERGY_WEIGHT = 1.0  # max points for energy; scaled by how close the values are


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences (the Scoring Rule).

    Uses the Algorithm Recipe:
      - genre match  -> +GENRE_WEIGHT (categorical: match/no-match)
      - mood match   -> +MOOD_WEIGHT  (categorical: match/no-match)
      - energy       -> reward closeness: ENERGY_WEIGHT * (1 - abs(diff))

    Each preference is optional, so this works with a partial profile like
    {"genre": "pop", "mood": "happy", "energy": 0.8}.

    Returns (score, reasons) where `reasons` explains the points awarded.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre — categorical match
    if "genre" in user_prefs and song.get("genre") == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT})")

    # Mood — categorical match
    if "mood" in user_prefs and song.get("mood") == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT})")

    # Energy — numeric closeness (1.0 = exact match, 0.0 = opposite ends)
    if "energy" in user_prefs and "energy" in song:
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        energy_points = ENERGY_WEIGHT * closeness
        score += energy_points
        reasons.append(
            f"energy close to {user_prefs['energy']} "
            f"(song {song['energy']}, +{energy_points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Recommends the top-k songs for a user (the Ranking Rule).

    Scores every song with score_song(), sorts by score (highest first), and
    returns the top k as (song_dict, score, explanation) tuples.
    """
    # Score every song, building the explanation from its reasons.
    scored = [
        (song, score, "; ".join(reasons) if reasons else "no matching preferences")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Rank highest-first and keep the top k.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
