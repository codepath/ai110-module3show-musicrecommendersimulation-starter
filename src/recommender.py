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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numerical fields to appropriate types
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Scoring recipe:
    # +2 points for genre match
    # +1.5 points for mood match
    # For each numerical feature (energy, tempo_bpm, valence, danceability, acousticness):
    #   Add up to 1 point, linearly decreasing as distance increases (1 - abs(user - song))
    def score_song(user_prefs, song):
        """Calculate a match score and explanation for a song given user preferences."""
        score = 0.0
        explanation = []
        # Genre match
        if song['genre'] == user_prefs.get('genre'):
            score += 2.0
            explanation.append('Genre match (+2)')
        # Mood match
        if song['mood'] == user_prefs.get('mood'):
            score += 1.5
            explanation.append('Mood match (+1.5)')
        # Numerical features
        for feature in ['energy', 'valence', 'danceability', 'acousticness']:
            if feature in user_prefs:
                diff = abs(song[feature] - user_prefs[feature])
                feature_score = 1.0 - diff  # max 1, min 0
                feature_score = max(0.0, feature_score)
                score += feature_score
                explanation.append(f"{feature} similarity (+{feature_score:.2f})")
        # Tempo (bpm) - scale difference to [0,1] using 200 bpm as max reasonable range
        if 'tempo_bpm' in user_prefs:
            diff = abs(song['tempo_bpm'] - user_prefs['tempo_bpm']) / 200.0
            feature_score = 1.0 - diff
            feature_score = max(0.0, feature_score)
            score += feature_score
            explanation.append(f"tempo_bpm similarity (+{feature_score:.2f})")
        return score, "; ".join(explanation)

    # Pythonic: list comprehension and sorted()
    results = [(song, *score_song(user_prefs, song)) for song in songs]
    top_k = sorted(results, key=lambda x: x[1], reverse=True)[:k]
    return top_k
