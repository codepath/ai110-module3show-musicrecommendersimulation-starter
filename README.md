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

Real-world platforms like Spotify and YouTube combine two approaches: collaborative filtering, which learns from what millions of similar users play, skip and save, and content-based filtering, which matches songs by their own attributes such as audio features and metadata. My version is purely content-based, since I have no listening history from other users. It prioritizes closeness over magnitude: for each numeric feature, a song earns more points the nearer it is to my user's target value, rather than simply having a higher or lower value. I weight energy, acousticness and valence most heavily because they separate the songs in my catalog best. I give mood a smaller bonus, and genre the smallest, because most genres appear only once in my data. Each song gets a score, and then I rank all songs by score and return the top K.

**`Song` features**

- `genre` (categorical)
- `mood` (categorical)
- `energy` (0–1)
- `valence` (0–1)
- `acousticness` (0–1)
- `tempo_bpm`, `danceability`, `title`, `artist` and `id` are loaded from the CSV. Tempo and danceability are not scored, because they largely repeat energy. The rest are for display and identification.

**`UserProfile` features**

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_valence`
- `target_acousticness`

**Scoring rule (per song)**

```
score = 0.35·sim(energy) + 0.25·sim(acousticness) + 0.20·sim(valence)
      + 0.12·[mood match] + 0.08·[genre match]

sim(f) = 1 − |song_f − user_f|
```

**Ranking rule:** sort all songs by score, highest first, and return the top K.

**Data flow plan**

```
INPUT                     PROCESS (the loop)                      OUTPUT
-----                     ------------------                      ------
User prefs      ──►   load songs.csv → list of Song         
 - favorite_genre         │
 - favorite_mood          ▼
 - target_energy      for each song in list:                 sort by score (desc)
 - target_valence       1. sim(energy)       = 1 − |Δ|              │
 - target_acousticness  2. sim(acousticness) = 1 − |Δ|              ▼
 - K                    3. sim(valence)      = 1 − |Δ|        Top K recommendations
                        4. mood match  → bonus                 (title, artist, score,
                        5. genre match → bonus                  why it matched)
                        6. weighted sum → score
                        7. keep (song, score, reasons)
```

Plan:

1. **Input:** define a `UserProfile` (hard-coded dict is fine at first) and a value for K.
2. **Load:** read `data/songs.csv` into a list of `Song` objects, converting numeric columns to floats.
3. **Score one song:** write `score_song(user, song)` that returns the score and a list of reasons (for example "energy close: 0.98"). Test it on 2–3 songs by hand first.
4. **Loop:** apply `score_song` to every song in the catalog.
5. **Rank:** sort by score descending and slice the first K.
6. **Output:** print each recommendation with its score and reasons.

**Algorithm Recipe**

| Component | Weight | Type | Why this weight |
|---|---|---|---|
| Energy similarity | 0.35 | continuous, 0–1 | Best separates calm from intense songs in the catalog |
| Acousticness similarity | 0.25 | continuous, 0–1 | Separates acoustic (folk, classical, lofi) from electronic (edm, metal) |
| Valence similarity | 0.20 | continuous, 0–1 | Captures positive versus dark feel, which overlaps with mood |
| Mood match | 0.12 | exact match, 0 or 1 | Useful signal, but a label match is all-or-nothing |
| Genre match | 0.08 | exact match, 0 or 1 | Smallest, because most genres appear only once in 18 songs |

The weights sum to 1.0, so every score falls between 0 and 1 and is easy to read. The numeric features are 80% of the score, and the two labels are 20%.

Worked example: a user wants `pop / happy`, energy 0.8, valence 0.8, acousticness 0.2.

- *Sunrise City* (pop, happy): 0.34 + 0.25 + 0.19 + 0.12 + 0.08 = **0.98**
- *Rooftop Lights* (indie pop, happy): 0.34 + 0.21 + 0.20 + 0.12 + 0 = **0.87**
- *Gym Hero* (pop, intense): 0.30 + 0.21 + 0.19 + 0 + 0.08 = **0.79**

*Rooftop Lights* beats *Gym Hero* even though only *Gym Hero* matches the genre, because the mood and the audio feel match better.

**Expected biases and limitations**

- **Genre is under-weighted on purpose, so a user who cares most about genre will be underserved.** Someone who only wants metal could still get a non-metal song ranked above a metal one if its numeric features are closer.
- **Exact string matching ignores near-matches.** "indie pop" earns nothing for a "pop" user, and "relaxed" earns nothing for a "chill" user, even though they are close in feel.
- **The system favors "average" taste profiles.** Because it rewards closeness to a target, users with extreme targets (energy 0.95, acousticness 0.02) have few songs to match, and users in the middle get many near-ties.
- **The catalog is tiny and uneven.** With 18 songs and mostly one song per genre, a genre or mood match often decides a single result, and the top K quickly fills with weak matches.
- **Energy, acousticness and valence are correlated.** They partly measure the same thing, so one underlying trait (for example "calm and acoustic") may be counted several times.
- **No history or diversity.** The same top songs appear every time for the same profile, and the top K can all be near-duplicates (for example three lofi tracks).
- **The weights are my judgment, not learned from data.** They reflect what I think matters in this catalog, so another designer's weights would rank songs differently.

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

Output of `python -m src.main` for the default pop / happy profile:

```
Loaded songs: 18

================================================================
TOP 5 RECOMMENDATIONS
Profile: pop / happy | energy 0.8 | valence 0.8 | acoustic 0.2
================================================================

#1  Sunrise City by Neon Echo
    Score: 0.98 / 1.00   [pop, happy]
    Why:
      - energy close to target: 0.82 vs 0.80 (+0.34)
      - acousticness close to target: 0.18 vs 0.20 (+0.24)
      - valence close to target: 0.84 vs 0.80 (+0.19)
      - mood match: happy (+0.12)
      - genre match: pop (+0.08)

#2  Rooftop Lights by Indigo Parade
    Score: 0.87 / 1.00   [indie pop, happy]
    Why:
      - energy close to target: 0.76 vs 0.80 (+0.34)
      - acousticness close to target: 0.35 vs 0.20 (+0.21)
      - valence close to target: 0.81 vs 0.80 (+0.20)
      - mood match: happy (+0.12)

#3  Gym Hero by Max Pulse
    Score: 0.79 / 1.00   [pop, intense]
    Why:
      - energy close to target: 0.93 vs 0.80 (+0.30)
      - acousticness close to target: 0.05 vs 0.20 (+0.21)
      - valence close to target: 0.77 vs 0.80 (+0.19)
      - genre match: pop (+0.08)

#4  Night Drive Loop by Neon Echo
    Score: 0.72 / 1.00   [synthwave, moody]
    Why:
      - energy close to target: 0.75 vs 0.80 (+0.33)
      - acousticness close to target: 0.22 vs 0.20 (+0.24)
      - valence close to target: 0.49 vs 0.80 (+0.14)

#5  Pulse Cathedral by Hyperlane
    Score: 0.70 / 1.00   [edm, euphoric]
    Why:
      - energy close to target: 0.94 vs 0.80 (+0.30)
      - acousticness close to target: 0.04 vs 0.20 (+0.21)
      - valence close to target: 0.73 vs 0.80 (+0.19)

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



