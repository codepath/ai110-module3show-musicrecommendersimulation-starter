import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# Core Algorithm Recipe weights (see README); they sum to 1.0
NUMERIC_WEIGHTS = {"energy": 0.35, "acousticness": 0.25, "valence": 0.20}
MOOD_WEIGHT = 0.12
GENRE_WEIGHT = 0.08

# Advanced feature weights. A feature only counts when the user sets its preference,
# and the final score is divided by the weights in use, so it always stays in 0-1.
POPULARITY_WEIGHT = 0.10    # pref "popularity": 0-100
DECADE_WEIGHT = 0.10        # pref "decade": e.g. 1990
DECADE_SPAN = 40            # a gap of 40 years or more earns nothing
TAGS_WEIGHT = 0.15          # pref "mood_tags": list of tags
INSTRUMENTAL_WEIGHT = 0.10  # pref "instrumentalness": 0-1
CLEAN_WEIGHT = 0.05         # pref "avoid_explicit": True


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
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: List[str] = field(default_factory=list)
    instrumentalness: float = 0.0
    explicit: bool = False

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
    int_fields = ("id", "popularity", "release_decade")
    float_fields = ("energy", "valence", "acousticness", "tempo_bpm", "danceability", "instrumentalness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for name in int_fields:
                row[name] = int(row[name])
            for name in float_fields:
                row[name] = float(row[name])
            row["explicit"] = bool(int(row["explicit"]))
            row["mood_tags"] = row["mood_tags"].split("|")
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Each part is (weight, similarity from 0 to 1, reason text, show when similarity is 0)
    parts: List[Tuple[float, float, str, bool]] = []

    # Numeric features: closeness to the target, sim = 1 - |song - target|
    for feature, weight in NUMERIC_WEIGHTS.items():
        if feature in user_prefs:
            sim = 1.0 - abs(song[feature] - user_prefs[feature])
            label = f"{feature} close to target: {song[feature]:.2f} vs {user_prefs[feature]:.2f}"
            parts.append((weight, sim, label, True))

    # Categorical features: exact match earns the full weight, otherwise nothing
    if "mood" in user_prefs:
        sim = 1.0 if user_prefs["mood"] == song["mood"] else 0.0
        parts.append((MOOD_WEIGHT, sim, f"mood match: {song['mood']}", False))
    if "genre" in user_prefs:
        sim = 1.0 if user_prefs["genre"] == song["genre"] else 0.0
        parts.append((GENRE_WEIGHT, sim, f"genre match: {song['genre']}", False))

    # Advanced features (only used when the user sets them)
    if "popularity" in user_prefs:
        sim = 1.0 - abs(song["popularity"] - user_prefs["popularity"]) / 100
        label = f"popularity close to target: {song['popularity']} vs {user_prefs['popularity']}"
        parts.append((POPULARITY_WEIGHT, sim, label, True))
    if "decade" in user_prefs:
        gap = abs(song["release_decade"] - user_prefs["decade"])
        sim = max(0.0, 1.0 - gap / DECADE_SPAN)
        label = f"release decade: {song['release_decade']}s vs {user_prefs['decade']}s"
        parts.append((DECADE_WEIGHT, sim, label, True))
    if user_prefs.get("mood_tags"):
        wanted = user_prefs["mood_tags"]
        matched = [tag for tag in wanted if tag in song["mood_tags"]]
        sim = len(matched) / len(wanted)
        parts.append((TAGS_WEIGHT, sim, f"mood tags match: {', '.join(matched)}", False))
    if "instrumentalness" in user_prefs:
        sim = 1.0 - abs(song["instrumentalness"] - user_prefs["instrumentalness"])
        label = (
            f"instrumentalness close to target: "
            f"{song['instrumentalness']:.2f} vs {user_prefs['instrumentalness']:.2f}"
        )
        parts.append((INSTRUMENTAL_WEIGHT, sim, label, True))
    if user_prefs.get("avoid_explicit"):
        sim = 0.0 if song["explicit"] else 1.0
        label = "explicit lyrics" if song["explicit"] else "clean lyrics"
        parts.append((CLEAN_WEIGHT, sim, label, True))

    # Scale by the weights in use so the score always falls between 0 and 1
    total_weight = sum(weight for weight, _, _, _ in parts)
    if total_weight == 0:
        return 0.0, []

    score = 0.0
    reasons: List[str] = []
    for weight, sim, label, show_if_zero in parts:
        points = weight * sim / total_weight
        score += points
        if sim > 0 or show_if_zero:
            reasons.append(f"{label} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Judge every song with score_song, then rank; sorted() leaves `songs` untouched
    scored = (
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    )
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
