from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
from collections import Counter

SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced": {
        "genre": 1.5,
        "mood": 1.5,
        "energy": 2.0,
        "acoustic": 1.0,
        "decade": 1.0,
        "tags": 1.0,
        "popularity": 0.75,
        "instrumentalness": 0.5,
        "liveness": 0.5,
        "speechiness": 0.5,
    },
    "genre_first": {
        "genre": 3.0,
        "mood": 1.0,
        "energy": 1.25,
        "acoustic": 0.75,
        "decade": 1.0,
        "tags": 0.5,
        "popularity": 0.5,
        "instrumentalness": 0.25,
        "liveness": 0.25,
        "speechiness": 0.25,
    },
    "mood_first": {
        "genre": 1.0,
        "mood": 3.0,
        "energy": 1.25,
        "acoustic": 0.75,
        "decade": 1.0,
        "tags": 1.5,
        "popularity": 0.5,
        "instrumentalness": 0.25,
        "liveness": 0.25,
        "speechiness": 0.25,
    },
    "energy_focused": {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 3.5,
        "acoustic": 0.75,
        "decade": 0.75,
        "tags": 0.5,
        "popularity": 0.5,
        "instrumentalness": 0.25,
        "liveness": 0.5,
        "speechiness": 0.5,
    },
}


def get_available_scoring_modes() -> List[str]:
    return list(SCORING_MODES.keys())


def get_mode_max_score(mode: str) -> float:
    weights = SCORING_MODES.get(mode.lower(), SCORING_MODES["balanced"])
    # Tag score is capped at 1.5 before weighting.
    return (
        weights["genre"]
        + weights["mood"]
        + weights["energy"]
        + weights["acoustic"]
        + weights["decade"]
        + (1.5 * weights["tags"])
        + weights["popularity"]
        + weights["instrumentalness"]
        + weights["liveness"]
        + weights["speechiness"]
    )

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
    release_year: int = 2015
    mood_tags: str = ""
    instrumentalness: float = 0.0
    liveness: float = 0.1
    speechiness: float = 0.05

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

    @staticmethod
    def _decade_from_year(year: int) -> int:
        return (year // 10) * 10

    @staticmethod
    def _safe_closeness(value: float, target: float) -> float:
        return max(0.0, 1.0 - abs(value - target))

    def _score_song(self, user: UserProfile, song: Song) -> float:
        score = 0.0

        if song.genre.strip().lower() == user.favorite_genre.strip().lower():
            score += 2.0

        if song.mood.strip().lower() == user.favorite_mood.strip().lower():
            score += 1.0

        score += 2.0 * self._safe_closeness(song.energy, user.target_energy)

        song_is_acoustic = song.acousticness >= 0.5
        if song_is_acoustic == user.likes_acoustic:
            score += 1.0

        # Advanced feature scoring from Challenge 1.
        preferred_decade = 2010
        song_decade = self._decade_from_year(song.release_year)
        decade_gap = abs(song_decade - preferred_decade) / 10.0
        score += max(0.0, 1.0 - 0.25 * decade_gap)

        score += 0.5 * (song.popularity / 100.0)
        score += 0.5 * song.instrumentalness

        preferred_liveness = 0.15
        score += 0.5 * self._safe_closeness(song.liveness, preferred_liveness)

        preferred_speechiness = 0.06
        score += 0.5 * self._safe_closeness(song.speechiness, preferred_speechiness)

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top k songs ranked by match to user preferences."""
        ranked = sorted(self.songs, key=lambda song: self._score_song(user, song), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song is recommended."""
        reasons = []
        if song.genre.strip().lower() == user.favorite_genre.strip().lower():
            reasons.append(f"genre match ({song.genre})")
        if song.mood.strip().lower() == user.favorite_mood.strip().lower():
            reasons.append(f"mood match ({song.mood})")
        if abs(song.energy - user.target_energy) <= 0.15:
            reasons.append(f"strong energy fit ({song.energy:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("acoustic preference match")
        if not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append("produced sound preference match")
        if song.mood_tags:
            reasons.append(f"mood tags: {song.mood_tags}")

        return ", ".join(reasons) if reasons else "Overall profile similarity"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    try:
        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
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
                    "popularity": int(row.get("popularity", 50)),
                    "release_year": int(row.get("release_year", 2015)),
                    "mood_tags": row.get("mood_tags", ""),
                    "instrumentalness": float(row.get("instrumentalness", 0.0)),
                    "liveness": float(row.get("liveness", 0.1)),
                    "speechiness": float(row.get("speechiness", 0.05)),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    scoring_mode: str = "balanced",
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def get_mode_weights(mode: str) -> Dict[str, float]:
        return SCORING_MODES.get(mode.lower(), SCORING_MODES["balanced"])

    def calculate_score(
        song: Dict,
        user_genre: str,
        user_mood: str,
        user_energy: float,
        user_acoustic: bool,
        preferred_decade: int,
        preferred_tags: set,
        target_popularity: float,
        weights: Dict[str, float],
    ) -> float:
        """Calculate a single song's score based on user preferences."""
        score = 0.0
        
        if song["genre"].strip().lower() == user_genre.strip().lower():
            score += weights["genre"]
        
        if song["mood"].strip().lower() == user_mood.strip().lower():
            score += weights["mood"]
        
        energy_diff = abs(song["energy"] - user_energy)
        energy_similarity = max(0.0, min(1.0, 1.0 - energy_diff))
        score += weights["energy"] * energy_similarity
        
        song_is_acoustic = song["acousticness"] >= 0.5
        if song_is_acoustic == user_acoustic:
            score += weights["acoustic"]

        # Advanced math-based rules.
        song_decade = (int(song.get("release_year", 2015)) // 10) * 10
        decade_gap = abs(song_decade - preferred_decade) / 10.0
        score += weights["decade"] * max(0.0, 1.0 - 0.25 * decade_gap)

        song_tags = {
            tag.strip().lower()
            for tag in str(song.get("mood_tags", "")).split("|")
            if tag.strip()
        }
        tag_overlap = len(song_tags & preferred_tags)
        score += weights["tags"] * min(1.5, 0.5 * tag_overlap)

        popularity = float(song.get("popularity", 50)) / 100.0
        popularity_closeness = max(0.0, 1.0 - abs(popularity - target_popularity))
        score += weights["popularity"] * popularity_closeness

        score += weights["instrumentalness"] * float(song.get("instrumentalness", 0.0))

        preferred_liveness = float(user_prefs.get("preferred_liveness", 0.15))
        liveness_closeness = max(0.0, 1.0 - abs(float(song.get("liveness", 0.1)) - preferred_liveness))
        score += weights["liveness"] * liveness_closeness

        preferred_speechiness = float(user_prefs.get("preferred_speechiness", 0.06))
        speechiness_closeness = max(0.0, 1.0 - abs(float(song.get("speechiness", 0.05)) - preferred_speechiness))
        score += weights["speechiness"] * speechiness_closeness
        
        return score
    
    def explain_score(
        song: Dict,
        score: float,
        user_genre: str,
        user_mood: str,
        user_energy: float,
        user_acoustic: bool,
        preferred_decade: int,
        preferred_tags: set,
        mode: str,
    ) -> str:
        """Generate a human-readable explanation for why a song scored well."""
        reasons = []
        
        if song["genre"].strip().lower() == user_genre.strip().lower():
            reasons.append(f"matches your genre ({song['genre']})")
        
        if song["mood"].strip().lower() == user_mood.strip().lower():
            reasons.append(f"matches your mood ({song['mood']})")
        
        energy_diff = abs(song["energy"] - user_energy)
        if energy_diff <= 0.15:
            reasons.append(f"energy is very close ({song['energy']:.2f})")
        elif energy_diff <= 0.35:
            reasons.append(f"energy is close ({song['energy']:.2f})")
        
        song_is_acoustic = song["acousticness"] >= 0.5
        if user_acoustic and song_is_acoustic:
            reasons.append("fits your acoustic preference")
        if not user_acoustic and not song_is_acoustic:
            reasons.append("fits your preference for produced sound")

        song_decade = (int(song.get("release_year", 2015)) // 10) * 10
        if song_decade == preferred_decade:
            reasons.append(f"from your preferred era ({song_decade}s)")

        song_tags = {
            tag.strip().lower()
            for tag in str(song.get("mood_tags", "")).split("|")
            if tag.strip()
        }
        overlap = sorted(song_tags & preferred_tags)
        if overlap:
            reasons.append("mood tags align: " + ", ".join(overlap))

        reasons.append(f"mode={mode}")
        
        if not reasons:
            return "Overall similarity to your profile"
        
        return ", ".join(reasons)
    
    user_genre = str(user_prefs.get("genre", "")).strip()
    user_mood = str(user_prefs.get("mood", "")).strip()
    user_energy = float(user_prefs.get("energy", 0.5))
    user_acoustic = bool(user_prefs.get("likes_acoustic", False))
    preferred_decade = int(user_prefs.get("preferred_decade", 2010))
    preferred_tags = {
        tag.strip().lower()
        for tag in user_prefs.get("preferred_mood_tags", [])
        if str(tag).strip()
    }
    target_popularity = float(user_prefs.get("target_popularity", 0.75))
    mode = str(scoring_mode).strip().lower()
    weights = get_mode_weights(mode)
    artist_diversity_penalty = float(user_prefs.get("artist_diversity_penalty", 0.9))
    genre_diversity_penalty = float(user_prefs.get("genre_diversity_penalty", 0.35))
    
    scored_songs = []
    for song in songs:
        score = calculate_score(
            song,
            user_genre,
            user_mood,
            user_energy,
            user_acoustic,
            preferred_decade,
            preferred_tags,
            target_popularity,
            weights,
        )
        explanation = explain_score(
            song,
            score,
            user_genre,
            user_mood,
            user_energy,
            user_acoustic,
            preferred_decade,
            preferred_tags,
            mode,
        )
        scored_songs.append((song, score, explanation))
    
    # Diversity-aware greedy reranking: once an artist/genre appears, additional
    # songs from the same source receive a penalty to increase variety.
    remaining = scored_songs[:]
    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Counter = Counter()
    genre_counts: Counter = Counter()

    while remaining and len(selected) < k:
        best_idx = 0
        best_adjusted = float("-inf")

        for idx, (song, base_score, explanation) in enumerate(remaining):
            artist_seen = artist_counts[song["artist"]]
            genre_seen = genre_counts[song["genre"]]
            adjusted_score = (
                base_score
                - artist_diversity_penalty * artist_seen
                - genre_diversity_penalty * genre_seen
            )
            if adjusted_score > best_adjusted:
                best_adjusted = adjusted_score
                best_idx = idx

        song, base_score, explanation = remaining.pop(best_idx)
        artist_seen = artist_counts[song["artist"]]
        genre_seen = genre_counts[song["genre"]]
        adjusted_score = (
            base_score
            - artist_diversity_penalty * artist_seen
            - genre_diversity_penalty * genre_seen
        )

        artist_counts[song["artist"]] += 1
        genre_counts[song["genre"]] += 1

        penalty_note = (
            f"diversity penalty: artist={artist_diversity_penalty * artist_seen:.2f}, "
            f"genre={genre_diversity_penalty * genre_seen:.2f}"
        )
        selected.append((song, adjusted_score, f"{explanation}, {penalty_note}"))

    return selected
