import csv
from collections import Counter
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class RankingStrategy:
    """
    One way of ranking songs (the "Strategy" pattern). Every strategy runs the
    same scoring steps and only changes how many points genre, mood and energy
    are worth. Each strategy's weights add up to 4.0, so scores stay on the same
    scale in every mode.
    """
    key: str
    name: str
    description: str
    genre_points: float
    mood_points: float
    energy_points: float

    @property
    def core_max(self) -> float:
        return self.genre_points + self.mood_points + self.energy_points


GENRE_FIRST = RankingStrategy(
    "genre-first", "Genre-First",
    "Staying in your favorite genre matters most.",
    genre_points=2.0, mood_points=1.0, energy_points=1.0,
)
MOOD_FIRST = RankingStrategy(
    "mood-first", "Mood-First",
    "Matching your mood matters most.",
    genre_points=1.0, mood_points=2.0, energy_points=1.0,
)
ENERGY_FOCUSED = RankingStrategy(
    "energy-focused", "Energy-Focused",
    "Matching your energy level matters most.",
    genre_points=1.0, mood_points=1.0, energy_points=2.0,
)

@dataclass(frozen=True)
class DiversityPenalty:
    """
    Lowers a song's score for every song already picked that shares its artist
    or its genre, so the top results are not all from one artist or one genre.
    The penalty stacks: a third song by the same artist is penalized twice.
    """
    artist_penalty: float = 0.75
    genre_penalty: float = 0.25


DEFAULT_DIVERSITY = DiversityPenalty()

STRATEGIES = {
    strategy.key: strategy for strategy in (GENRE_FIRST, MOOD_FIRST, ENERGY_FOCUSED)
}
DEFAULT_STRATEGY = ENERGY_FOCUSED


def get_strategy(key: str) -> RankingStrategy:
    """Looks up a ranking strategy by its key, such as "mood-first"."""
    cleaned = key.strip().lower().replace("_", "-")
    if cleaned not in STRATEGIES:
        raise ValueError(
            f"Unknown ranking mode '{key}'. Choose from: {', '.join(STRATEGIES)}"
        )
    return STRATEGIES[cleaned]


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
    def __init__(
        self,
        songs: List[Song],
        strategy: RankingStrategy = DEFAULT_STRATEGY,
        diversity: Optional[DiversityPenalty] = None,
    ):
        self.songs = songs
        self.strategy = strategy
        self.diversity = diversity

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the user, ranked by score from highest to lowest."""
        prefs = _prefs_from_profile(user)
        by_dict = {id(song.__dict__): song for song in self.songs}
        results = recommend_songs(
            prefs, [song.__dict__ for song in self.songs], k, self.strategy, self.diversity
        )
        return [by_dict[id(song_dict)] for song_dict, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns the scoring reasons for a song as one "; "-separated string."""
        _, reasons = score_song(_prefs_from_profile(user), song.__dict__, self.strategy)
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

def max_score(user_prefs: Dict, strategy: RankingStrategy = DEFAULT_STRATEGY) -> float:
    """
    Highest score a song can earn for these preferences. It is 4.0 for a basic
    profile in any mode and grows by each advanced preference the user supplied.
    """
    total = strategy.core_max
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

def score_song(
    user_prefs: Dict, song: Dict, strategy: RankingStrategy = DEFAULT_STRATEGY
) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Recipe: the strategy sets the points for a genre match, a mood match, and
    energy closeness (energy_points * (1 - |song energy - target energy|)). The
    default strategy is +1.0 genre, +1.0 mood and up to +2.0 energy. The target
    energy is clamped to [0, 1] so the total stays within [0, core_max].

    Optional advanced preferences add more points: "mood_tags" (up to +1.0),
    "popularity", "decade", "language" and "instrumentalness" (up to +0.5 each).
    They only count when supplied, and max_score() gives the matching ceiling.
    Returns (score, reasons).
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += strategy.genre_points
        reasons.append(f"genre match: {song['genre']} (+{strategy.genre_points:.1f})")

    if song["mood"] == user_prefs["mood"]:
        score += strategy.mood_points
        reasons.append(f"mood match: {song['mood']} (+{strategy.mood_points:.1f})")

    target_energy = min(1.0, max(0.0, user_prefs["energy"]))
    energy_points = strategy.energy_points * (1 - abs(song["energy"] - target_energy))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target_energy:.2f} "
        f"(+{energy_points:.2f})"
    )

    extra_points, extra_reasons = _advanced_points(user_prefs, song)
    score += extra_points
    reasons.extend(extra_reasons)

    return score, reasons

def _pick_diverse(
    candidates: List[Tuple[Dict, float, List[str]]],
    k: int,
    diversity: DiversityPenalty,
) -> List[Tuple[Dict, float, str]]:
    """
    Picks k songs one at a time. Before each pick, every remaining song loses
    points for each already-picked song with the same artist or genre. The
    adjusted score never drops below 0. Ties go to the song that ranked higher
    before any penalty. Candidates must be sorted best first.
    """
    remaining = list(candidates)
    picked = []
    artists, genres = Counter(), Counter()

    while remaining and len(picked) < k:
        best = None  # (adjusted score, index, penalty note)
        for index, (song, score, _) in enumerate(remaining):
            artist_repeats = artists[song.get("artist")]
            genre_repeats = genres[song.get("genre")]
            penalty = (
                diversity.artist_penalty * artist_repeats
                + diversity.genre_penalty * genre_repeats
            )
            adjusted = max(0.0, score - penalty)
            if best is None or adjusted > best[0]:
                note = None
                if penalty:
                    parts = []
                    if artist_repeats:
                        parts.append(f"artist {song['artist']} already picked {artist_repeats}x")
                    if genre_repeats:
                        parts.append(f"genre {song['genre']} already picked {genre_repeats}x")
                    note = f"diversity penalty: {', '.join(parts)} (-{score - adjusted:.2f})"
                best = (adjusted, index, note)

        adjusted, index, note = best
        song, _, reasons = remaining.pop(index)
        artists[song.get("artist")] += 1
        genres[song.get("genre")] += 1
        picked.append((song, adjusted, "; ".join(reasons + ([note] if note else []))))
    return picked


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: RankingStrategy = DEFAULT_STRATEGY,
    diversity: Optional[DiversityPenalty] = None,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Pass a DiversityPenalty to avoid filling the top k with one artist or genre.
    With no penalty, the result is simply the k highest scores.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        scored.append((song, score, reasons))
    scored.sort(key=lambda item: item[1], reverse=True)
    if diversity is not None:
        return _pick_diverse(scored, k, diversity)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
