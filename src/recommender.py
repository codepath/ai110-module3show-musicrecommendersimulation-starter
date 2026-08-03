import csv
from typing import List, Dict, Tuple, Optional, Iterable, Any
from dataclasses import dataclass

# --- Scoring weights -------------------------------------------------------
# A matching genre is worth more than a matching mood, which in turn is
# weighted alongside how closely the song's energy matches the user's target.
GENRE_WEIGHT = 3.0
MOOD_WEIGHT = 2.0
ENERGY_WEIGHT = 2.0
ACOUSTIC_WEIGHT = 1.0

# Numeric fields loaded from the CSV that should be parsed as floats.
NUMERIC_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

# Features used ONLY for the objective genre/mood similarity fallback.
# Deliberately excludes energy and acousticness (already scored directly) so
# nothing is double-counted. tempo_bpm is scaled to 0-1; valence and
# danceability are already on a 0-1 scale.
SIMILARITY_FIELDS = ("tempo_bpm", "valence", "danceability")

# A non-exact genre/mood match only earns a spoken "sounds similar" reason
# once its similarity clears this bar (it still contributes points below it).
SIMILARITY_REASON_THRESHOLD = 0.5

# --- Preference vocabulary -------------------------------------------------
# Out-of-vocabulary genre/mood labels are mapped onto an existing catalog
# label so a requested term the catalog has never heard of ("k-pop", "sad")
# still resolves to a real, data-derived centroid instead of silently scoring
# zero. Values MUST match a catalog label exactly (case-sensitive).
GENRE_SYNONYMS = {
    "kpop": "pop", "k-pop": "pop", "j-pop": "pop", "jpop": "pop",
    "electropop": "pop", "dance pop": "pop", "power pop": "pop",
    "hip-hop": "hip hop", "rap": "hip hop", "trap": "hip hop",
    "punk": "rock", "grunge": "rock", "hard rock": "rock", "alt rock": "rock",
    "heavy metal": "metal", "death metal": "metal", "thrash": "metal",
    "chillhop": "lofi", "lo-fi": "lofi", "lofi hip hop": "lofi",
    "soul": "R&B", "rnb": "R&B", "r&b": "R&B", "neo-soul": "R&B",
    "house": "EDM", "techno": "EDM", "dubstep": "EDM", "edm": "EDM",
    "dance": "EDM", "electronic": "EDM",
    "singer-songwriter": "folk", "acoustic": "folk",
}
MOOD_SYNONYMS = {
    "sad": "melancholic", "melancholy": "melancholic", "down": "melancholic",
    "blue": "melancholic", "depressed": "melancholic", "somber": "melancholic",
    "euphoric": "uplifting", "elated": "uplifting", "hopeful": "uplifting",
    "joyful": "happy", "cheerful": "happy", "upbeat": "happy",
    "angry": "aggressive", "furious": "aggressive", "rage": "aggressive",
    "calm": "chill", "peaceful": "relaxed", "mellow": "relaxed",
    "sleepy": "dreamy", "tense": "intense",
}

# Genre buckets used only to pick an honest word for the non-acoustic sound.
HEAVY_GENRES = {"rock", "metal", "punk", "grunge"}
ELECTRONIC_GENRES = {"EDM", "synthwave", "pop", "indie pop", "hip hop", "R&B"}


def _resolve_label(requested: Optional[str], centroids: Dict[str, Any],
                   synonyms: Dict[str, str]) -> Tuple[Optional[str], bool]:
    """
    Resolve a requested genre/mood label to one that has a data-derived
    centroid. Returns (canonical_label, was_remapped):
      - already a real catalog label   -> (label, False)
      - a known synonym of a real one  -> (mapped_label, True)
      - otherwise                      -> (requested, False)  # scores nothing
    """
    if not requested:
        return requested, False
    if requested in centroids:
        return requested, False
    mapped = synonyms.get(requested.strip().lower())
    if mapped and mapped in centroids:
        return mapped, True
    return requested, False


def _produced_sound_phrase(genre: str) -> str:
    """Pick an honest descriptor for a non-acoustic track based on its genre."""
    if genre in HEAVY_GENRES:
        return "amplified, heavy sound"
    if genre in ELECTRONIC_GENRES:
        return "produced/electronic sound"
    return "clean, produced sound"


def _build_explanation(reasons: List[str], caveats: List[str]) -> str:
    """Combine positive reasons and honest caveats into one readable line."""
    main = ", ".join(reasons) if reasons else "no strong match, but it's a reasonable option"
    if caveats:
        main += " — note: " + "; ".join(caveats)
    return main


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


def _read(song: Any, field: str, default: Any = None) -> Any:
    """Read a field from either a Song dataclass or a plain dict."""
    if isinstance(song, dict):
        return song.get(field, default)
    return getattr(song, field, default)


def _as_features(song: Any) -> Dict[str, Any]:
    """Normalize a Song or dict into a uniform feature dict of the right types."""
    return {
        "genre": _read(song, "genre", "") or "",
        "mood": _read(song, "mood", "") or "",
        "energy": float(_read(song, "energy", 0.0) or 0.0),
        "acousticness": float(_read(song, "acousticness", 0.0) or 0.0),
        "tempo_bpm": float(_read(song, "tempo_bpm", 0.0) or 0.0),
        "valence": float(_read(song, "valence", 0.0) or 0.0),
        "danceability": float(_read(song, "danceability", 0.0) or 0.0),
    }


class CatalogStats:
    """
    Objective, data-derived statistics used for the genre/mood similarity
    fallback. All numbers come from the catalog itself -- nothing is
    hand-tuned. Centroids are the average feature vector of every song sharing
    a given genre (or mood), computed over SIMILARITY_FIELDS.
    """

    def __init__(self, songs: Iterable[Any]):
        """Derive tempo scaling bounds and per-genre/mood centroids from the catalog."""
        feats = [_as_features(s) for s in songs]
        tempos = [f["tempo_bpm"] for f in feats]
        # tempo is scaled to 0-1 using the catalog's own min/max (data-driven).
        self.tempo_min = min(tempos) if tempos else 0.0
        self.tempo_max = max(tempos) if tempos else 0.0
        self.genre_centroids = self._centroids(feats, "genre")
        self.mood_centroids = self._centroids(feats, "mood")

    def _norm_vec(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Scale the similarity features to 0-1 (only tempo needs scaling)."""
        span = self.tempo_max - self.tempo_min
        tempo_n = (features["tempo_bpm"] - self.tempo_min) / span if span else 0.0
        return {
            "tempo_bpm": tempo_n,
            "valence": features["valence"],
            "danceability": features["danceability"],
        }

    def _centroids(self, feats: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, float]]:
        """Average the normalized similarity features of every song sharing each genre/mood label."""
        groups: Dict[str, List[Dict[str, float]]] = {}
        for f in feats:
            groups.setdefault(f[key], []).append(self._norm_vec(f))
        centroids: Dict[str, Dict[str, float]] = {}
        for label, vecs in groups.items():
            centroids[label] = {
                field: sum(v[field] for v in vecs) / len(vecs)
                for field in SIMILARITY_FIELDS
            }
        return centroids

    def similarity(self, features: Dict[str, Any], centroid: Dict[str, float]) -> float:
        """
        Objective closeness in 0-1: 1 minus the mean absolute difference
        between this song's normalized features and a centroid.
        """
        vec = self._norm_vec(features)
        mean_diff = sum(abs(vec[f] - centroid[f]) for f in SIMILARITY_FIELDS) / len(SIMILARITY_FIELDS)
        return 1.0 - mean_diff


def _score_attributes(
    *,
    features: Dict[str, Any],
    favorite_genre: Optional[str],
    favorite_mood: Optional[str],
    target_energy: Optional[float],
    likes_acoustic: bool,
    stats: Optional[CatalogStats] = None,
) -> Tuple[float, List[str], List[str]]:
    """
    Core content-based scoring shared by the functional and OOP APIs.

    Genre and mood use additive partial credit: an exact match earns the full
    weight; a non-exact match earns weight x similarity, where similarity is an
    objective, data-derived closeness to the favorite genre's/mood's centroid
    (see CatalogStats). An out-of-vocabulary request (e.g. "sad", "k-pop") is
    first mapped through a synonym table onto an existing catalog label so it
    still scores against a real centroid. With no stats provided, only exact
    matches score.

    Returns (score, reasons, caveats): reasons are positive contributors;
    caveats are honest disclosures about preferences this song could NOT honor.
    """
    score = 0.0
    reasons: List[str] = []
    caveats: List[str] = []
    genre = features["genre"]
    mood = features["mood"]

    genre_centroids = stats.genre_centroids if stats else {}
    mood_centroids = stats.mood_centroids if stats else {}

    # Resolve out-of-vocabulary requests onto a real, data-derived centroid.
    fav_genre, genre_remapped = _resolve_label(favorite_genre, genre_centroids, GENRE_SYNONYMS)
    fav_mood, mood_remapped = _resolve_label(favorite_mood, mood_centroids, MOOD_SYNONYMS)

    # Genre: exact match (after synonym resolution) earns full weight;
    # otherwise partial credit by objective similarity to the genre's centroid.
    if favorite_genre:
        g_txt = f'{fav_genre} (interpreted from "{favorite_genre}")' if genre_remapped else fav_genre
        if genre == fav_genre:
            score += GENRE_WEIGHT
            reasons.append(f"matches your favorite genre ({g_txt})")
        elif fav_genre in genre_centroids:
            # Square the similarity so strong matches stay strong while mediocre
            # ones are pushed down -- keeps exact matches clearly ahead and
            # re-widens the ranking, without a hard cap.
            sim = stats.similarity(features, genre_centroids[fav_genre]) ** 2
            score += GENRE_WEIGHT * sim
            if sim >= SIMILARITY_REASON_THRESHOLD:
                # Honest wording: this is an audio-texture match, not a genre match.
                reasons.append(f"has a similar audio profile (tempo, valence, danceability) to {g_txt}")
            else:
                caveats.append(f'this is a different genre than the "{favorite_genre}" you asked for')
        else:
            # Requested, but the catalog has nothing like it and no synonym fit.
            caveats.append(f'the catalog has nothing tagged "{favorite_genre}", so genre could not be matched')

    # Mood: same additive scheme, same synonym resolution.
    if favorite_mood:
        m_txt = f'{fav_mood} (interpreted from "{favorite_mood}")' if mood_remapped else fav_mood
        if mood == fav_mood:
            score += MOOD_WEIGHT
            reasons.append(f"fits the {m_txt} mood you like")
        elif fav_mood in mood_centroids:
            sim = stats.similarity(features, mood_centroids[fav_mood]) ** 2
            score += MOOD_WEIGHT * sim
            if sim >= SIMILARITY_REASON_THRESHOLD:
                reasons.append(f"has a feel similar to the {m_txt} mood")
        else:
            caveats.append(f'the catalog has no "{favorite_mood}" mood, so mood could not be matched')

    # Energy: reward closeness to the target (both are on a 0-1 scale).
    if target_energy is not None:
        energy = features["energy"]
        score += ENERGY_WEIGHT * (1.0 - abs(energy - target_energy))
        if abs(energy - target_energy) <= 0.2:
            reasons.append("energy level is close to what you want")

    # Acousticness: reward high values for acoustic lovers, low values
    # otherwise. When the preference clearly can't be met, say so instead of
    # staying silent.
    acousticness = features["acousticness"]
    acoustic_fit = acousticness if likes_acoustic else (1.0 - acousticness)
    score += ACOUSTIC_WEIGHT * acoustic_fit
    if likes_acoustic:
        if acousticness >= 0.6:
            reasons.append("has the acoustic sound you prefer")
        elif acousticness <= 0.4:
            caveats.append("this isn't an acoustic track, unlike your stated preference")
    else:
        if acousticness <= 0.4:
            reasons.append(f"has the {_produced_sound_phrase(genre)} you prefer")
        elif acousticness >= 0.6:
            caveats.append("this is more acoustic/organic than you usually pick")

    return score, reasons, caveats


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog and derive its similarity stats once for reuse."""
        self.songs = songs
        # Centroids/stats are derived once from the catalog and reused.
        self._stats = CatalogStats(songs) if songs else None

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str], List[str]]:
        """Score one song for a user, returning (score, reasons, caveats)."""
        return _score_attributes(
            features=_as_features(song),
            favorite_genre=user.favorite_genre,
            favorite_mood=user.favorite_mood,
            target_energy=user.target_energy,
            likes_acoustic=user.likes_acoustic,
            stats=self._stats,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs for a user, ranked by score descending."""
        ranked = sorted(
            self.songs,
            key=lambda song: self._score(user, song)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Build a human-readable one-line explanation of a song's score for a user."""
        score, reasons, caveats = self._score(user, song)
        return f"{song.title} (score {score:.2f}): " + _build_explanation(reasons, caveats) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song["id"] = int(song["id"])
            for field in NUMERIC_FIELDS:
                if field in song and song[field] != "":
                    song[field] = float(song[field])
            songs.append(song)
    return songs


def score_ceiling(user_prefs: Dict, songs: Optional[List[Dict]] = None) -> float:
    """
    Maximum score achievable for these preferences, counting only terms that
    can actually contribute. A genre/mood the catalog cannot match (even after
    synonym resolution) is excluded from the ceiling, so a song matched purely
    on audio features still normalizes to a high fraction instead of being
    dragged down by an unmatchable request. Used for display only -- it does
    not affect ranking. Pass `songs` to resolve genre/mood against the catalog.
    """
    stats = CatalogStats(songs) if songs else None
    genre_centroids = stats.genre_centroids if stats else {}
    mood_centroids = stats.mood_centroids if stats else {}

    ceiling = ACOUSTIC_WEIGHT  # acousticness always contributes something
    fav_genre, _ = _resolve_label(user_prefs.get("genre"), genre_centroids, GENRE_SYNONYMS)
    if fav_genre in genre_centroids:
        ceiling += GENRE_WEIGHT
    fav_mood, _ = _resolve_label(user_prefs.get("mood"), mood_centroids, MOOD_SYNONYMS)
    if fav_mood in mood_centroids:
        ceiling += MOOD_WEIGHT
    if user_prefs.get("energy") is not None:
        ceiling += ENERGY_WEIGHT
    return ceiling


def score_song(user_prefs: Dict, song: Dict, catalog: Optional[List[Dict]] = None) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    user_prefs keys (all optional): "genre", "mood", "energy", "likes_acoustic".
    Pass `catalog` (the full song list) to enable the objective genre/mood
    similarity fallback; without it, only exact genre/mood matches score.
    Returns (score, reasons); any honest caveats are appended to reasons as
    "note: ..." entries so this two-value contract is preserved.
    """
    stats = CatalogStats(catalog) if catalog else None
    score, reasons, caveats = _score_attributes(
        features=_as_features(song),
        favorite_genre=user_prefs.get("genre"),
        favorite_mood=user_prefs.get("mood"),
        target_energy=user_prefs.get("energy"),
        likes_acoustic=bool(user_prefs.get("likes_acoustic", False)),
        stats=stats,
    )
    return score, reasons + [f"note: {c}" for c in caveats]


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Returns a list of (song_dict, score, explanation) sorted by score desc.
    """
    # Build the data-derived stats once and reuse across all songs.
    stats = CatalogStats(songs) if songs else None

    scored = []
    for song in songs:
        score, reasons, caveats = _score_attributes(
            features=_as_features(song),
            favorite_genre=user_prefs.get("genre"),
            favorite_mood=user_prefs.get("mood"),
            target_energy=user_prefs.get("energy"),
            likes_acoustic=bool(user_prefs.get("likes_acoustic", False)),
            stats=stats,
        )
        explanation = _build_explanation(reasons, caveats)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
