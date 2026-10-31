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

Real-world platforms like Spotify and YouTube combine two signals. Collaborative filtering learns from the behavior of millions of users ("people like you also liked this"), and content-based filtering compares the attributes of the songs themselves. This simulation is content-based only. It has no listening history from other users, so it compares each song's attributes to one user's stated taste. It scores each song on the user's preferred **genre**, **mood**, and **energy**.

### Song features

Each `Song` stores:

- `genre` and `mood` (categories)
- `energy`, `valence`, `danceability`, `acousticness` (0.0 to 1.0)
- `tempo_bpm` (beats per minute)
- `id`, `title`, `artist` (identifying info, not used for scoring)

### UserProfile features

Each `UserProfile` stores:

- `favorite_genre`
- `favorite_mood`
- `target_energy` (0.0 to 1.0)
- `likes_acoustic` (True or False)

### How a song is scored

Each song gets a score from 0 to 4.0 by adding up three parts:

- **Genre:** +2.0 if the song's genre matches the user's favorite genre, otherwise 0.
- **Mood:** +1.0 if the song's mood matches the user's favorite mood, otherwise 0.
- **Energy:** up to +1.0 based on how close the song is to `target_energy`, using `1.0 * (1 - |song energy - target energy|)`. A song is not rewarded for simply having more energy.

Genre is weighted twice as heavily as mood, so a genre match with the wrong mood (2.0 plus energy) beats a mood match with the wrong genre (1.0 plus energy). Energy never outweighs a category match on its own. It breaks ties between songs that match the same categories.

### How songs are chosen

The `Recommender` scores every song in the catalog, sorts them from highest to lowest score, and returns the top `k` (5 by default). Each result includes a short explanation of why it was picked.

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

Running `python -m src.main` with the starter profile (genre=pop, mood=happy, energy=0.8):

```
================================================================
                       MUSIC RECOMMENDER
================================================================
Profile: genre=pop, mood=happy, energy=0.8
Top 5 recommendations
----------------------------------------------------------------

#1  Sunrise City  by Neon Echo
    Score: 3.98 / 4.00
    Reasons:
      - genre match: pop (+2.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.80 (+0.98)

#2  Gym Hero  by Max Pulse
    Score: 2.87 / 4.00
    Reasons:
      - genre match: pop (+2.0)
      - energy 0.93 vs target 0.80 (+0.87)

#3  Rooftop Lights  by Indigo Parade
    Score: 1.96 / 4.00
    Reasons:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.80 (+0.96)

#4  Concrete Crown  by Kid Meridian
    Score: 0.98 / 4.00
    Reasons:
      - energy 0.78 vs target 0.80 (+0.98)

#5  Fuego en la Noche  by Luna Caliente
    Score: 0.95 / 4.00
    Reasons:
      - energy 0.85 vs target 0.80 (+0.95)

================================================================
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



