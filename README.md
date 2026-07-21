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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real platforms blend collaborative filtering (predicting your taste from what similar users liked) with content-based filtering (matching a song's own attributes — genre, mood, energy — to your stated preferences). Spotify and TikTok lean on collaborative filtering at scale for its cultural pattern-matching, but use content-based signals for new songs and explainability. My version is purely content-based: no other users, just a direct comparison between a song's attributes and one UserProfile. Each Song uses genre and mood (exact-match categorical features) plus energy and acousticness (numeric 0–1 features scored by closeness to a target). Each UserProfile mirrors this with favorite_genre, favorite_mood, target_energy, and likes_acoustic. Genre matches are weighted highest, mood next, then the two numeric closeness scores — the Recommender sums these into a score per song and ranks the catalog to produce the top-N list. I left out tempo_bpm and danceability (they track energy too closely) and valence (overlaps with mood) as candidates for later experiments.

**Overview.** This is a purely *content-based* recommender: there are no other users and no collaborative filtering. It compares each song's own attributes against a single `UserProfile` and ranks the catalog by how well they match.

**The catalog.** `data/songs.csv` holds 18 songs. Each has categorical tags (`genre`, `mood`) and numeric audio features on a 0.0–1.0 scale (`energy`, `valence`, `danceability`, `acousticness`) plus `tempo_bpm`.

**Song features used.** `genre` and `mood` (categorical, scored by exact match) and `energy` and `acousticness` (numeric, scored by closeness). `tempo_bpm` and `danceability` are left out (they track `energy`) and `valence` is left out (overlaps `mood`) — kept as later experiments.

**UserProfile.** Stores `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`. The sample profile is `synthwave` / `energetic` / `target_energy=0.75` / `likes_acoustic=False`.

### Algorithm Recipe

The `Recommender` scores every song against the `UserProfile` as the sum of:

| Signal | Points | How it's measured |
|---|---|---|
| Genre match | +2.0 | `song.genre == favorite_genre` |
| Mood match | +1.0 | `song.mood == favorite_mood` |
| Energy closeness | up to +1.0 | `1 − abs(song.energy − target_energy)` |
| Acousticness fit | +0.5 | `song.acousticness` agrees with `likes_acoustic` |

Songs are sorted by total score (highest first) and the top *K* are returned, each with a short reason listing which signals matched.

**Worked example.** For the sample profile, *"Night Drive Loop"* (synthwave, moody, energy 0.75, acousticness 0.22) scores +2.0 (genre) + 0 (mood) + 1.0 (energy on target) + 0.5 (low acousticness matches `likes_acoustic=False`) = **3.5**, near the top.

### Potential biases

- **Genre over-prioritization:** Genre's +2.0 weight lets a genre-only match outrank a better mood/energy fit tagged differently — a "filter bubble."
- **Exact-match blind spots:** Close tags like "pop" vs "indie pop" score zero on genre.
- **Tiny catalog:** With 18 songs, one genre/mood can dominate, and unseen tastes can't surface.

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



