import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm recipe: core max score is 4.0 (1.0 genre + 1.0 mood + 2.0 energy).
GENRE_POINTS = 1.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 2.0

# Advanced features. Each one only counts when the user gives that preference,
# so a basic profile still has a max score of 4.0 (see max_score).
TAG_POINTS = 1.0            # share of the user's mood tags the song has
POPULARITY_POINTS = 0.5     # closeness on a 0-100 scale
DECADE_POINTS = 0.5         # closeness in release decade
LANGUAGE_POINTS = 0.5       # exact language match
INSTRUMENTAL_POINTS = 0.5   # closeness on a 0-1 scale
DECADE_SPAN = 30            # years apart at which decade points reach 0

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
    # Advanced features (optional so older code that builds a Song still works)
    popularity: Optional[int] = None            # 0-100
    release_decade: Optional[int] = None        # e.g. 1990
    mood_tags: Optional[List[str]] = None       # e.g. ["nostalgic", "warm"]
    language: Optional[str] = None              # e.g. "english"
    instrumentalness: Optional[float] = None    # 0.0 (vocals) to 1.0 (no vocals)

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
    # Advanced preferences (optional; leave as None to skip that part of scoring)
    target_popularity: Optional[int] = None
    preferred_decade: Optional[int] = None
    preferred_mood_tags: Optional[List[str]] = None
    preferred_language: Optional[str] = None
    target_instrumentalness: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the user, ranked by score from highest to lowest."""
        prefs = _prefs_from_profile(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, song.__dict__)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns the scoring reasons for a song as one "; "-separated string."""
        _, reasons = score_song(_prefs_from_profile(user), song.__dict__)
        return "; ".join(reasons)


def _prefs_from_profile(user: UserProfile) -> Dict:
    """Converts a UserProfile into the prefs dict that score_song expects."""
    prefs = {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
    }
    optional = {
        "popularity": user.target_popularity,
        "decade": user.preferred_decade,
        "mood_tags": user.preferred_mood_tags,
        "language": user.preferred_language,
        "instrumentalness": user.target_instrumentalness,
    }
    prefs.update({key: value for key, value in optional.items() if value is not None})
    return prefs

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = ("id", "popularity", "release_decade")
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability", "acousticness",
        "instrumentalness",
    )
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                if row.get(field):
                    row[field] = int(row[field])
            for field in float_fields:
                if row.get(field):
                    row[field] = float(row[field])
            if row.get("mood_tags"):
                row["mood_tags"] = row["mood_tags"].split("|")
            songs.append(row)
    return songs

def max_score(user_prefs: Dict) -> float:
    """
    Highest score a song can earn for these preferences. It is 4.0 for a basic
    profile and grows by each advanced preference the user actually supplied.
    """
    total = GENRE_POINTS + MOOD_POINTS + ENERGY_POINTS
    if user_prefs.get("mood_tags"):
        total += TAG_POINTS
    if user_prefs.get("popularity") is not None:
        total += POPULARITY_POINTS
    if user_prefs.get("decade") is not None:
        total += DECADE_POINTS
    if user_prefs.get("language"):
        total += LANGUAGE_POINTS
    if user_prefs.get("instrumentalness") is not None:
        total += INSTRUMENTAL_POINTS
    return total

def _advanced_points(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Points for the advanced features. A feature is skipped when the user did not
    ask for it or the song has no value for it.
    """
    points = 0.0
    reasons = []

    wanted = {tag.strip().lower() for tag in user_prefs.get("mood_tags") or []}
    if wanted and song.get("mood_tags"):
        have = {tag.lower() for tag in song["mood_tags"]}
        hits = sorted(wanted & have)
        earned = TAG_POINTS * len(hits) / len(wanted)
        points += earned
        reasons.append(
            f"mood tags {len(hits)}/{len(wanted)} matched: "
            f"{', '.join(hits) or 'none'} (+{earned:.2f})"
        )

    if user_prefs.get("popularity") is not None and song.get("popularity") is not None:
        target = min(100, max(0, user_prefs["popularity"]))
        earned = POPULARITY_POINTS * (1 - abs(song["popularity"] - target) / 100)
        points += earned
        reasons.append(
            f"popularity {song['popularity']} vs target {target} (+{earned:.2f})"
        )

    if user_prefs.get("decade") is not None and song.get("release_decade") is not None:
        gap = abs(song["release_decade"] - user_prefs["decade"])
        earned = DECADE_POINTS * max(0.0, 1 - gap / DECADE_SPAN)
        points += earned
        reasons.append(
            f"decade {song['release_decade']}s vs {user_prefs['decade']}s (+{earned:.2f})"
        )

    language = (user_prefs.get("language") or "").strip().lower()
    if language and song.get("language") and song["language"].lower() == language:
        points += LANGUAGE_POINTS
        reasons.append(f"language match: {song['language']} (+{LANGUAGE_POINTS:.1f})")

    if (
        user_prefs.get("instrumentalness") is not None
        and song.get("instrumentalness") is not None
    ):
        target = min(1.0, max(0.0, user_prefs["instrumentalness"]))
        earned = INSTRUMENTAL_POINTS * (1 - abs(song["instrumentalness"] - target))
        points += earned
        reasons.append(
            f"instrumentalness {song['instrumentalness']:.2f} vs target "
            f"{target:.2f} (+{earned:.2f})"
        )

    return points, reasons

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Recipe: +1.0 genre match, +1.0 mood match, and up to +2.0 for energy
    closeness (2 * (1 - |song energy - target energy|)). The target energy is
    clamped to [0, 1] so the energy term stays within [0, 2] and the total
    stays within [0, 4].

    Optional advanced preferences add more points: "mood_tags" (up to +1.0),
    "popularity", "decade", "language" and "instrumentalness" (up to +0.5 each).
    They only count when supplied, and max_score() gives the matching ceiling.
    Returns (score, reasons).
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if song["mood"] == user_prefs["mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    target_energy = min(1.0, max(0.0, user_prefs["energy"]))
    energy_points = ENERGY_POINTS * (1 - abs(song["energy"] - target_energy))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target_energy:.2f} "
        f"(+{energy_points:.2f})"
    )

    extra_points, extra_reasons = _advanced_points(user_prefs, song)
    score += extra_points
    reasons.extend(extra_reasons)

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
