from typing import List, Dict, Tuple
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


def _score_song_dict(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append("genre match")

    if song["mood"].lower() == user_prefs["mood"].lower():
        score += 1.5
        reasons.append("mood match")

    energy_diff = abs(song["energy"] - user_prefs["energy"])
    energy_score = max(0.0, 2.0 - (energy_diff * 2))
    score += energy_score
    reasons.append(f"energy diff {energy_diff:.2f}")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acoustic_score = song["acousticness"]
    else:
        acoustic_score = 1.0 - song["acousticness"]

    score += acoustic_score

    if likes_acoustic:
        reasons.append("matches acoustic preference")
    else:
        reasons.append("matches non-acoustic preference")

    explanation = ", ".join(reasons)
    return score, explanation


def _score_song_object(song: Song, user: UserProfile) -> float:
    score = 0.0

    if song.genre.lower() == user.favorite_genre.lower():
        score += 2.0

    if song.mood.lower() == user.favorite_mood.lower():
        score += 1.5

    energy_diff = abs(song.energy - user.target_energy)
    score += max(0.0, 2.0 - (energy_diff * 2))

    if user.likes_acoustic:
        score += song.acousticness
    else:
        score += 1.0 - song.acousticness

    return score


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []

        for song in self.songs:
            score = _score_song_object(song, user)
            scored_songs.append((song, score))

        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre match")

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood match")

        energy_diff = abs(song.energy - user.target_energy)
        reasons.append(f"energy diff {energy_diff:.2f}")

        if user.likes_acoustic:
            reasons.append("user likes acoustic songs")
        else:
            reasons.append("user prefers less acoustic songs")

        return "Recommended because of " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

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

    return songs


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []

    for song in songs:
        score, explanation = _score_song_dict(song, user_prefs)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]