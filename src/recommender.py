import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# CSV columns that must be converted from text to numbers when loading.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

# Scoring weights (Algorithm Recipe in README.md). Change these to run experiments.
GENRE_EXACT_POINTS = 2.0
GENRE_PARTIAL_POINTS = 1.0
MOOD_POINTS = 1.0
NUMERIC_WEIGHT = 1.0  # max points for each closeness / acoustic rule
NUMERIC_FEATURES = ("energy", "valence", "danceability")
# Best possible score when every preference is given (genre + mood + 3 numeric + acoustic).
MAX_SCORE = GENRE_EXACT_POINTS + MOOD_POINTS + NUMERIC_WEIGHT * (len(NUMERIC_FEATURES) + 1)

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
    """Read the songs CSV into a list of dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in INT_FIELDS:
                row[field] = int(row[field])
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # 1. Genre: exact match, or partial match when one name contains the other.
    user_genre = str(user_prefs.get("favorite_genre", "")).strip().lower()
    song_genre = str(song["genre"]).strip().lower()
    if user_genre and song_genre == user_genre:
        score += GENRE_EXACT_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_EXACT_POINTS:.1f})")
    elif user_genre and (user_genre in song_genre or song_genre in user_genre):
        score += GENRE_PARTIAL_POINTS
        reasons.append(
            f"related genre: {song['genre']} ~ {user_prefs['favorite_genre']} "
            f"(+{GENRE_PARTIAL_POINTS:.1f})"
        )

    # 2. Mood: exact match only.
    user_mood = str(user_prefs.get("favorite_mood", "")).strip().lower()
    if user_mood and str(song["mood"]).strip().lower() == user_mood:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    # 3. Numeric closeness: reward songs NEAR the target, not the highest values.
    for feature in NUMERIC_FEATURES:
        target = user_prefs.get(f"target_{feature}")
        if target is None:
            continue  # optional target not given -> skip this rule
        points = max(0.0, 1.0 - abs(target - song[feature])) * NUMERIC_WEIGHT
        if points > 0:
            score += points
            reasons.append(
                f"{feature} {song[feature]:.2f} vs target {target:.2f} (+{points:.2f})"
            )

    # 4. Acoustic fit: acoustic lovers get acousticness, others get its opposite.
    if "likes_acoustic" in user_prefs:
        likes = bool(user_prefs["likes_acoustic"])
        points = (song["acousticness"] if likes else 1.0 - song["acousticness"]) * NUMERIC_WEIGHT
        if points > 0:
            score += points
            label = "acoustic" if likes else "produced/electronic"
            reasons.append(f"{label} sound, acousticness {song['acousticness']:.2f} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank them highest first, and return the top k as (song, score, explanation)."""
    # 1. Judge: one (song, score, reasons) tuple per song.
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # 2. Rank: highest score first. sorted() is stable, so ties keep catalog order,
    #    and it returns a new list, so `songs` itself is never reordered.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # 3. Pick: top k, turning each reasons list into a readable explanation.
    return [
        (song, score, "; ".join(reasons) or "no strong match with your preferences")
        for song, score, reasons in ranked[:k]
    ]
