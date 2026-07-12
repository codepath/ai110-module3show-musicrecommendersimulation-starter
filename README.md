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

Real-world recommenders like Spotify and YouTube predict what you'll enjoy by learning
from huge amounts of data. They mostly combine two ideas: collaborative filtering
("people with taste similar to yours also liked this") and content-based filtering
("this song is similar to songs you already like"). They also watch your behavior —
skips, replays, and how long you listen — and adjust over time. My version is a small,
simplified **content-based** recommender. Instead of using millions of users, it looks
only at the musical features of each song (things like energy, mood, and tempo) and
compares them to a profile of what the user likes. It prioritizes *closeness of taste*:
songs whose features are near the user's preferred values score highest. I chose this
approach because it's easy to understand, works on a tiny catalog with no other users,
and clearly shows how raw data becomes a ranked list of recommendations.

### What each `Song` uses

- `genre` (categorical, e.g. lofi, pop, rock)
- `mood` (categorical, e.g. chill, happy, intense)
- `energy` (0–1)
- `valence` — positivity/happiness (0–1)
- `danceability` (0–1)
- `acousticness` (0–1)
- `tempo_bpm` — **normalized to 0–1 before scoring**

`id`, `title`, and `artist` are stored for display only and are not scored.

### What the `UserProfile` stores

- Preferred `genre` and `mood`
- Target values (0–1) for energy, valence, danceability, acousticness, and tempo
  (computed as the average of songs the user has liked)
- **Per-feature weights** — how much each feature matters (e.g. energy weighted higher
  than acousticness)
- A list of songs already heard, so they can be excluded from recommendations

### Two example profiles

| Profile | genre | mood | energy | acoustic | tempo | notes |
|---|---|---|---|---|---|---|
| **Focus / Study** | lofi | focused | 0.35 | 0.80 | ~75 BPM | high weight on energy + acousticness; danceability weight ~0 |
| **Workout** | pop | intense | 0.90 | 0.10 | ~150 BPM | high weight on energy + tempo |

Running both over the same catalog makes the recommendations flip — proof the system
responds to *where* the user's taste sits.

### Algorithm Recipe

1. **Normalize tempo** for every song: `tempo_norm = tempo_bpm / 200` (puts all numeric
   features on a shared 0–1 scale so no single feature dominates the score).
2. **Score each song (Scoring Rule).** For every numeric feature, reward closeness:
   `feature_score = 1 - abs(song_value - profile_target)`.
   For each categorical feature (genre, mood), score `1` on a match, `0` otherwise.
3. **Combine into one number** with a weighted average:
   `total = Σ (weight · feature_score) / Σ weights`.
4. **Rank the list (Ranking Rule).** Drop songs already heard, sort by `total` (highest
   first), and return the top *N*. (Optional: cap songs per genre so the list stays
   diverse.)

### Potential biases I expect

- **Over-prioritizing heavily-weighted features.** Because the Focus profile weights
  energy and acousticness so highly, it may bury great *mood-matched* songs (e.g. an
  ambient or jazz track perfect for studying) just for having the "wrong" acousticness.
- **Genre as a hard match.** Scoring genre as match/no-match gives no partial credit,
  so a lofi-lover never sees a closely-related ambient track — the system can trap a
  user inside a single genre.
- **Specialist blind spot.** A single-region profile separates opposite vibes well
  (chill lofi vs. intense rock) but can't tell energetic genres apart — rock, metal, and
  EDM all just read as "not chill" and cluster at the bottom.
- **Tiny catalog.** With only ~18 songs, a few tracks can dominate every recommendation,
  which is not realistic.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



