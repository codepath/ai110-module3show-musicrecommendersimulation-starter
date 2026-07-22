import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Weights for each component of the score. They sum to 1.0 so that a "perfect"
# song (all preferences satisfied) scores 1.0 and each weight is directly
# interpretable as "how much this attribute matters."
WEIGHT_GENRE = 0.35
WEIGHT_MOOD = 0.30
WEIGHT_ENERGY = 0.25
WEIGHT_ACOUSTIC = 0.10

# Spread of the energy Gaussian. Smaller = pickier about matching target energy.
ENERGY_SIGMA = 0.15

# A song counts as "acoustic" when its acousticness is above this threshold.
ACOUSTIC_THRESHOLD = 0.6

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
    Loads songs from a CSV file into a list of dictionaries.

    Numeric attributes are converted from strings to floats so they can be
    used directly by the scoring algorithm (e.g. the energy Gaussian). The
    categorical fields (title, artist, genre, mood) are left as strings.

    Required by src/main.py
    """
    # Columns that must be numeric for the scoring algorithm.
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user's preferences.

    Strategy (philosophy one: only score what the user asked for):
      - genre    : categorical, 1.0 on exact match else 0.0
      - mood     : categorical, 1.0 on exact match else 0.0
      - energy   : continuous, Gaussian on the distance to the target energy
      - acoustic : boolean, 1.0 when the song's acoustic-ness agrees with the
                   user's like/dislike of acoustic tracks

    Each component is scored in [0, 1], multiplied by its weight, and summed.
    A component is only included when the user actually expresses that
    preference, so missing preferences neither help nor penalize a song.

    Returns a tuple of (score, reasons), where reasons is a list of
    human-readable strings such as "genre match: pop (+0.35)".

    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # --- Genre: exact categorical match ---
    if "genre" in user_prefs:
        if song["genre"] == user_prefs["genre"]:
            contribution = WEIGHT_GENRE * 1.0
            score += contribution
            reasons.append(f"genre match: {song['genre']} (+{contribution:.2f})")

    # --- Mood: exact categorical match ---
    if "mood" in user_prefs:
        if song["mood"] == user_prefs["mood"]:
            contribution = WEIGHT_MOOD * 1.0
            score += contribution
            reasons.append(f"mood match: {song['mood']} (+{contribution:.2f})")

    # --- Energy: Gaussian on distance to the target ---
    if "energy" in user_prefs:
        distance = song["energy"] - user_prefs["energy"]
        energy_match = math.exp(-(distance ** 2) / (2 * ENERGY_SIGMA ** 2))
        contribution = WEIGHT_ENERGY * energy_match
        score += contribution
        reasons.append(
            f"energy close to {user_prefs['energy']:.2f} (+{contribution:.2f})"
        )

    # --- Acoustic: boolean preference agrees with the song ---
    if "likes_acoustic" in user_prefs:
        song_is_acoustic = song["acousticness"] > ACOUSTIC_THRESHOLD
        if song_is_acoustic == user_prefs["likes_acoustic"]:
            contribution = WEIGHT_ACOUSTIC * 1.0
            score += contribution
            label = "acoustic" if song_is_acoustic else "non-acoustic"
            reasons.append(f"{label} as preferred (+{contribution:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
