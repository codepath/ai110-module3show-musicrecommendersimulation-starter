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
    target_valence: float = 0.5
    target_acousticness: float = 0.5
    genre_strictness: float = 0.6  # 0=flexible, 1=strict


# ============================================================================
# USER PROFILE EXAMPLES
# ============================================================================

def create_chill_lofi_lover() -> Dict:
    """
    Profile: User who loves relaxed, acoustic lofi music.
    Perfect for studying or sleeping.
    """
    return {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.60,
        "target_acousticness": 0.80,
        "acousticness_weight": 1.0,     # [UPDATED: was 1.5] to reduce acoustic-only bias
        "likes_acoustic": True,
        "genre_strictness": 0.7
    }


def create_intense_rock_fan() -> Dict:
    """
    Profile: User who loves energetic, intense rock music.
    Perfect for workouts or emotional expression.
    """
    return {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.50,
        "target_acousticness": 0.15,
        "acousticness_weight": 0.5,
        "likes_acoustic": False,
        "genre_strictness": 0.6
    }


def create_jazz_soul_lover() -> Dict:
    """Jazz/soul connoisseur who loves smooth, organic sounds with relaxed vibes."""
    return {
        "favorite_genre": "jazz",
        "favorite_mood": "relaxed",
        "target_energy": 0.45,
        "target_valence": 0.60,
        "target_acousticness": 0.80,
        "acousticness_weight": 1.2,
        "likes_acoustic": True,
        "genre_strictness": 0.5
    }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommend top-k songs for a user based on their profile.
        Scores all songs and returns the highest-scoring ones.
        """
        if not self.songs:
            return []
        
        # Convert UserProfile to dictionary for score_song()
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy,
            'target_valence': user.target_valence,
            'target_acousticness': user.target_acousticness,
            'acousticness_weight': 1.0,  # Default weight
        }
        
        # Score all songs
        scored_songs = []
        for song in self.songs:
            # Convert Song to dictionary for score_song()
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness,
            }
            
            score, reasons = score_song(user_prefs, song_dict)
            scored_songs.append((song, score, reasons))
        
        # Sort by score (descending)
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k Song objects
        return [song for song, score, reasons in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explain why a song was recommended to a user.
        Returns a string with the scoring reasons.
        """
        # Convert UserProfile to dictionary
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy,
            'target_valence': user.target_valence,
            'target_acousticness': user.target_acousticness,
            'acousticness_weight': 1.0,  # Default weight
        }
        
        # Convert Song to dictionary
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
        }
        
        score, reasons = score_song(user_prefs, song_dict)
        explanation = " + ".join(reasons)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from CSV file and returns list of song dictionaries."""
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song and returns (score, reasons) tuple with detailed breakdown."""
    score = 0.0
    reasons = []
    scores_breakdown = {}  # Track individual component scores
    
    # LEVEL 1: Categorical matches (strong signals)
    # Genre match: +1.0 point (reduced from 1.5 to allow numeric features to compete)
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 1.0
        reasons.append("Genre match")
    
    # Mood match: +1.0 point
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 1.0
        reasons.append("Mood match")
    
    # LEVEL 2: Weighted similarity (numeric - gradual)
    # CHECK FOR CONFLICTING ATTRIBUTES (NEW)
    # Energy and valence should be somewhat aligned
    energy_valence_conflict = abs(user_prefs['target_energy'] - (1 - user_prefs['target_valence']))
    conflict_penalty = 1.0
    if energy_valence_conflict > 0.6:
        conflict_penalty = 0.8  # Apply 20% penalty
        reasons.append("[CONFLICT] Energy and mood contradict")
    scores_breakdown['conflict_penalty'] = conflict_penalty
    
    # Energy: Very important for both profiles
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = 1.5 * (1.0 - energy_diff) * conflict_penalty
    score += energy_score
    scores_breakdown['energy'] = round(energy_score, 2)
    
    # Energy precision bonus: +0.5 if energy_diff < 0.05 (NEW)
    if energy_diff < 0.05:
        score += 0.5
        reasons.append(f"Perfect energy ({song['energy']:.2f})")
    elif energy_diff < 0.15:
        reasons.append(f"Good energy match ({song['energy']:.2f})")
    
    # Valence: Moderately important
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = 0.75 * (1.0 - valence_diff)
    score += valence_score
    scores_breakdown['valence'] = round(valence_score, 2)
    
    # Acousticness: Varies by profile (weighted)
    acoustic_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    acoustic_weight = user_prefs.get('acousticness_weight', 1.0)
    acoustic_score = acoustic_weight * (1.0 - acoustic_diff)
    score += acoustic_score
    scores_breakdown['acousticness'] = round(acoustic_score, 2)
    
    # Check acousticness reason
    if acoustic_diff < 0.1:
        if song['acousticness'] > 0.7:
            reasons.append("High acousticness")
        elif song['acousticness'] < 0.2:
            reasons.append("Low acousticness (electric)")
    
    # Add default reason if no reasons found
    if not reasons:
        reasons.append("Good overall match")
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return top-k song recommendations scored and ranked by user preference match."""
    if not songs:
        return []
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)  # New signature
        explanation = " + ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (descending)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-k
    return scored_songs[:k]
