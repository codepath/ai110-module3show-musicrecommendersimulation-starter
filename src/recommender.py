from typing import List, Dict, Tuple
import csv
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

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if user.favorite_genre and song.genre == user.favorite_genre:
            score += 1.0
            reasons.append(f"genre match ({user.favorite_genre}) (+1.0)")

        if user.favorite_mood and song.mood == user.favorite_mood:
            score += 1.0
            reasons.append(f"mood match ({user.favorite_mood}) (+1.0)")

        if user.target_energy is not None:
            proximity_score = (1.0 - abs(song.energy - user.target_energy)) * 2.0
            score += proximity_score
            reasons.append(f"energy proximity ({proximity_score/2.0:.2f}) (+{proximity_score:.2f})")

        if user.likes_acoustic is not None:
            is_acoustic = song.acousticness > 0.5
            if is_acoustic == user.likes_acoustic:
                score += 0.5
                reasons.append("acoustic preference match (+0.5)")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_candidates = []
        for song in self.songs:
            score, _ = self._score(user, song)
            scored_candidates.append((song, score))
        
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_candidates[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numerical values to appropriate types
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # 1. Genre Match (+2.0) - High Priority
    target_genre = user_prefs.get('genre') or user_prefs.get('favorite_genre')
    if target_genre and song.get('genre') == target_genre:
        score += 1.0
        reasons.append(f"genre match ({target_genre}) (+1.0)")

    # 2. Mood Match (+1.0) - Medium Priority
    target_mood = user_prefs.get('mood') or user_prefs.get('favorite_mood')
    if target_mood and song.get('mood') == target_mood:
        score += 1.0
        reasons.append(f"mood match ({target_mood}) (+1.0)")

    # 3. Energy Proximity (Up to +1.0) - Medium Priority
    target_energy = user_prefs.get('energy') or user_prefs.get('target_energy')
    if target_energy is not None:
        song_energy = song.get('energy', 0.5)
        proximity_score = (1.0 - abs(song_energy - target_energy)) * 2.0
        score += proximity_score
        reasons.append(f"energy proximity ({proximity_score/2.0:.2f}) (+{proximity_score:.2f})")

    # 4. Acoustic Preference (+0.5) - Low Priority
    likes_acoustic = user_prefs.get('likes_acoustic')
    if likes_acoustic is not None:
        is_acoustic = song.get('acousticness', 0) > 0.5
        if is_acoustic == likes_acoustic:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_candidates = []
    
    # 1. THE LOOP: Score every song in the catalog
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_candidates.append((song, score, explanation))
    
    # 2. THE RANKING: Sort songs from highest to lowest score
    # We use .sort() here to modify our candidate list directly
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # 3. THE OUTPUT: Return the top k results
    return scored_candidates[:k]
