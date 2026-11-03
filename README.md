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

Real-world platforms like Spotify and YouTube blend collaborative filtering (learning from what millions of listeners play, skip, and save) with content-based filtering (matching the audio traits of songs), then rank the candidates. My version has no listening history, so it is purely content-based. It compares each song's attributes to a user's stated taste and prioritizes how *close* a song is to what the user wants, not whether its values are high or low. Energy and mood matter most, followed by acousticness, valence, and genre.

**`Song` features**

- `genre`
- `mood`
- `energy`
- `acousticness`
- `valence`
- `tempo_bpm` and `danceability` (stored, but given little or no weight because they overlap with energy)

**`UserProfile` features**

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `likes_acoustic` (maps to a high or low acousticness target)
- `target_valence` (planned addition)

**Scoring and ranking**

- Each song gets a score from 0 to 1. Numeric features score `1 - |song - target|`, and genre and mood add a bonus for an exact match.
- Weights: energy 0.30, mood 0.25, acousticness 0.20, valence 0.15, genre 0.10.
- Songs are then sorted by score and the top K are returned.

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



