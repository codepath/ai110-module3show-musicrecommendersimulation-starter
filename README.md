# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube generally combine two strategies: **collaborative filtering** (recommending things that *other, similar users* liked) and **content-based filtering** (recommending things that share *attributes* with what a specific user already likes). This simulation implements the second approach only — there's no shared user-interaction data here, just one user's stated preferences compared against each song's own attributes.

My version prioritizes categorical matches (`genre`, `mood`) as the strongest signal of taste, since they're more stable indicators of what a user likes than moment-to-moment numeric closeness. Numeric features (`energy`, `acousticness`) are scored by how close they are to the user's target, not by whether they're simply higher or lower — a user who wants `target_energy=0.4` shouldn't get the highest-energy songs in the catalog, just the closest ones.

**`Song` features used:** `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

**`UserProfile` fields used:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

**Scoring Rule** (per song): each feature contributes points to a running total —
- `genre` match: **+2.0** if `song.genre == user.favorite_genre`, else 0
- `mood` match: **+1.0** if `song.mood == user.favorite_mood`, else 0
- `energy` closeness: **+1.0 × (1 - abs(song.energy - user.target_energy))** — a perfect match earns the full 1.0, and points fall off linearly as the song drifts from the user's target
- `acousticness` match: **+0.5** if `song.acousticness > 0.6` and `user.likes_acoustic` is `True`, or if `song.acousticness < 0.4` and `user.likes_acoustic` is `False`; else 0

The song's total score is the sum of these components (max 4.5). Genre outweighs mood because it's the more stable signal of taste; mood still gets a full extra point since it captures context the genre alone can't; energy is capped at 1.0 so it can nudge the ranking without overriding a categorical mismatch; acousticness gets the smallest weight since it's a secondary preference, not a stated favorite.

**Ranking Rule** (per list): all songs are scored individually, then sorted by score descending, and the top `k` are returned as the recommendations.

**Data Flow Plan:**

```
INPUT
  UserProfile (favorite_genre, favorite_mood, target_energy, likes_acoustic)
  songs.csv → load_songs() → List[Song]
        │
        ▼
PROCESS  (the loop — once per Song)
  for song in songs:
      score = 0
      score += 2.0  if song.genre == user.favorite_genre
      score += 1.0  if song.mood  == user.favorite_mood
      score += 1.0 * (1 - abs(song.energy - user.target_energy))
      score += 0.5  if acousticness matches user.likes_acoustic
      reasons = [ ...which of the above fired... ]
      → (song, score, reasons)
        │
        ▼
OUTPUT  (the ranking)
  sort all (song, score, reasons) by score, descending
  take top k
  → List[(song, score, explanation)]
```
**Algorithm Recipe** (per song): each feature contributes points to a running total —
- `genre` match: **+2.0** if `song.genre == user.favorite_genre`, else 0
- `mood` match: **+1.0** if `song.mood == user.favorite_mood`, else 0
- `energy` closeness: **+1.0 × (1 - abs(song.energy - user.target_energy))** — a perfect match earns the full 1.0, and points fall off linearly as the song drifts from the user's target
- `acousticness` match: **+0.5** if `song.acousticness > 0.6` and `user.likes_acoustic` is `True`, or if `song.acousticness < 0.4` and `user.likes_acoustic` is `False`; else 0

**Expected Biases:** This system might over-prioritize genre, ignoring great mood or energy matches from songs in a different genre — a `chill` song a user would love could rank below a mediocre song that merely shares their `favorite_genre`. It may also underrepresent artists or genres that appear rarely in the catalog (e.g. `data/songs.csv` has only one song per genre in most cases), since a single bad or unmatched attribute can knock a song out of contention with no similar alternatives to fall back on.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default starter profile (`genre=pop, mood=happy, energy=0.8`):

```
Loading songs from data/songs.csv...
Loaded songs: 18

Top recommendations for genre=pop, mood=happy, energy=0.8
=========================================================

1. Sunrise City by Neon Echo - Score: 4.48
   - genre match (pop) (+2.0)
   - mood match (happy) (+1.0)
   - energy closeness (+0.98)
   - non-acoustic preference match (+0.5)

2. Gym Hero by Max Pulse - Score: 3.37
   - genre match (pop) (+2.0)
   - energy closeness (+0.87)
   - non-acoustic preference match (+0.5)

3. Rooftop Lights by Indigo Parade - Score: 2.46
   - mood match (happy) (+1.0)
   - energy closeness (+0.96)
   - non-acoustic preference match (+0.5)

4. Block Party Anthem by MC Tempo - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)

5. Night Drive Loop by Neon Echo - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Weight Shift: halve genre (2.0 → 1.0), double energy (1.0 → 2.0)

I temporarily changed the weight constants at the top of `recommender.py` (`GENRE_WEIGHT`, `ENERGY_WEIGHT`) to test how sensitive the rankings are to the genre/energy balance. The max possible score stayed the same (1.0 + 1.0 + 2.0 + 0.5 = 4.5, same as the original 2.0 + 1.0 + 1.0 + 0.5 = 4.5), so scores from this run are still on the same scale as the finalized recipe — a useful sanity check that the math was still valid before comparing results.

**What stayed the same:** for profiles where one song matched both genre and mood (`Sunrise City` for High-Energy Pop, `Library Rain` for Chill Lofi, `Storm Runner` for Deep Intense Rock), that song was still #1 — a double categorical match is strong enough to win under either weighting.

**What changed:**
- The **#2 vs #3 gap shrank** in several lists. For High-Energy Pop, `Rooftop Lights` (mood match only, genre mismatch) closed from 1.11 points behind `Gym Hero` (genre match only) down to a 0.22-point gap — energy closeness now counts for much more, so a strong energy fit can nearly cancel out a genre mismatch.
- In the **"Genre Not In Catalog"** adversarial profile, a new song (`Island Drift`, reggae, energy=0.50 — a perfect match to the 0.5 target) entered the top 5 purely on a perfect energy score, something that never happened under the original weights.
- In the **"Conflicting Signals (Energetic + Sad)"** adversarial profile, `Rainy Window Blues` — the only `blues` song, which won #1 under the original recipe on genre match alone — fell out of the top 5 entirely. Its own energy (0.30) is very far from the profile's target (0.9), and with energy now weighted double, that mismatch outweighed the halved genre bonus.

**More accurate, or just different?** Mostly just different, with one case that arguably improved: `Rainy Window Blues` topping a list despite a huge energy mismatch (under the original weights) felt like an artifact of the catalog only having one blues song, not a genuinely good recommendation — the weight shift fixed that specific case. But this comes at a cost to the system's stated design goal (see "How The System Works"): genre and mood are supposed to be prioritized as the *more stable* signal of taste precisely because numeric closeness is more moment-to-moment. Doubling energy's weight undercuts that intentional design choice. I reverted to the original weights (`GENRE_WEIGHT=2.0`, `ENERGY_WEIGHT=1.0`) as the finalized recipe, but this is a real tension worth revisiting with a larger, more evenly distributed catalog.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



