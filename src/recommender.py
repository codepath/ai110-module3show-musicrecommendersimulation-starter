import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_against_profile(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a Song against a UserProfile, returning (total_score, list_of_reasons)."""
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append(f"genre match: {song.genre} (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append(f"mood match: {song.mood} (+1.0)")

    energy_similarity = 1.0 - abs(user.target_energy - song.energy)
    score += energy_similarity
    reasons.append(f"energy proximity: {energy_similarity:.2f} (song={song.energy:.2f}, target={user.target_energy:.2f})")

    if user.likes_acoustic and song.acousticness >= 0.6:
        score += 0.5
        reasons.append(f"acoustic vibe match (+0.5)")
    elif not user.likes_acoustic and song.acousticness < 0.4:
        score += 0.3
        reasons.append(f"low-acousticness match (+0.3)")

    return score, reasons


class Recommender:
    """OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top-k sorted by score."""
        scored = [
            (song, _score_song_against_profile(user, song)[0])
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        _, reasons = _score_song_against_profile(user, song)
        if not reasons:
            return "No strong attribute match found, but included for variety."
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed numeric values."""
    print(f"Loading songs from {csv_path}...")
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
    return songs


def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song dict against a user preferences dict, returning (score, explanation)."""
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    target_energy = float(user_prefs.get("energy", 0.5))
    energy_similarity = 1.0 - abs(target_energy - float(song["energy"]))
    score += energy_similarity
    reasons.append(f"energy proximity: {energy_similarity:.2f}")

    explanation = "; ".join(reasons) if reasons else "no strong attribute match"
    return score, explanation


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs by user preferences, returning the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        s, explanation = _score_song_dict(user_prefs, song)
        scored.append((song, s, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
