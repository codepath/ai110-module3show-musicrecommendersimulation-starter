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

Output from the first version of the runner, for a single pop / happy profile (energy 0.8). `src/main.py` now runs six profiles, and their output is in [Experiments You Tried](#experiments-you-tried):

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

Each profile below was run with `python -m src.main`. The first three are typical listeners and the last three are adversarial profiles built to trick the scoring.

### Standard profiles

**High-Energy Pop**

```
================================================================
PROFILE: High-Energy Pop
pop / happy | energy 0.9 | valence 0.85 | acoustic 0.1
================================================================

#1  Sunrise City by Neon Echo
    Score: 0.95 / 1.00   [pop, happy]
    Why:
      - energy close to target: 0.82 vs 0.90 (+0.32)
      - acousticness close to target: 0.18 vs 0.10 (+0.23)
      - valence close to target: 0.84 vs 0.85 (+0.20)
      - mood match: happy (+0.12)
      - genre match: pop (+0.08)

#2  Gym Hero by Max Pulse
    Score: 0.84 / 1.00   [pop, intense]
    Why:
      - energy close to target: 0.93 vs 0.90 (+0.34)
      - acousticness close to target: 0.05 vs 0.10 (+0.24)
      - valence close to target: 0.77 vs 0.85 (+0.18)
      - genre match: pop (+0.08)

#3  Rooftop Lights by Indigo Parade
    Score: 0.80 / 1.00   [indie pop, happy]
    Why:
      - energy close to target: 0.76 vs 0.90 (+0.30)
      - acousticness close to target: 0.35 vs 0.10 (+0.19)
      - valence close to target: 0.81 vs 0.85 (+0.19)
      - mood match: happy (+0.12)

#4  Pulse Cathedral by Hyperlane
    Score: 0.75 / 1.00   [edm, euphoric]
    Why:
      - energy close to target: 0.94 vs 0.90 (+0.34)
      - acousticness close to target: 0.04 vs 0.10 (+0.23)
      - valence close to target: 0.73 vs 0.85 (+0.18)

#5  Storm Runner by Voltline
    Score: 0.72 / 1.00   [rock, intense]
    Why:
      - energy close to target: 0.91 vs 0.90 (+0.35)
      - acousticness close to target: 0.10 vs 0.10 (+0.25)
      - valence close to target: 0.48 vs 0.85 (+0.13)
================================================================
```

Matches intuition: the pop/happy track wins, then the other pop track, then the happy indie pop track. *Gym Hero* ranks second even though its mood is "intense", because its energy and genre match.

**Chill Lofi**

```
================================================================
PROFILE: Chill Lofi
lofi / chill | energy 0.4 | valence 0.6 | acoustic 0.8
================================================================

#1  Library Rain by Paper Lanterns
    Score: 0.97 / 1.00   [lofi, chill]
    Why:
      - energy close to target: 0.35 vs 0.40 (+0.33)
      - acousticness close to target: 0.86 vs 0.80 (+0.24)
      - valence close to target: 0.60 vs 0.60 (+0.20)
      - mood match: chill (+0.12)
      - genre match: lofi (+0.08)

#2  Midnight Coding by LoRoom
    Score: 0.96 / 1.00   [lofi, chill]
    Why:
      - energy close to target: 0.42 vs 0.40 (+0.34)
      - acousticness close to target: 0.71 vs 0.80 (+0.23)
      - valence close to target: 0.56 vs 0.60 (+0.19)
      - mood match: chill (+0.12)
      - genre match: lofi (+0.08)

#3  Focus Flow by LoRoom
    Score: 0.87 / 1.00   [lofi, focused]
    Why:
      - energy close to target: 0.40 vs 0.40 (+0.35)
      - acousticness close to target: 0.78 vs 0.80 (+0.24)
      - valence close to target: 0.59 vs 0.60 (+0.20)
      - genre match: lofi (+0.08)

#4  Spacewalk Thoughts by Orbit Bloom
    Score: 0.84 / 1.00   [ambient, chill]
    Why:
      - energy close to target: 0.28 vs 0.40 (+0.31)
      - acousticness close to target: 0.92 vs 0.80 (+0.22)
      - valence close to target: 0.65 vs 0.60 (+0.19)
      - mood match: chill (+0.12)

#5  Coffee Shop Stories by Slow Stereo
    Score: 0.74 / 1.00   [jazz, relaxed]
    Why:
      - energy close to target: 0.37 vs 0.40 (+0.34)
      - acousticness close to target: 0.89 vs 0.80 (+0.23)
      - valence close to target: 0.71 vs 0.60 (+0.18)
================================================================
```

Works well. Both lofi/chill tracks lead, and the next three (lofi/focused, ambient/chill, jazz/relaxed) are sensible neighbors.

**Deep Intense Rock**

```
================================================================
PROFILE: Deep Intense Rock
rock / intense | energy 0.92 | valence 0.45 | acoustic 0.08
================================================================

#1  Storm Runner by Voltline
    Score: 0.99 / 1.00   [rock, intense]
    Why:
      - energy close to target: 0.91 vs 0.92 (+0.35)
      - acousticness close to target: 0.10 vs 0.08 (+0.24)
      - valence close to target: 0.48 vs 0.45 (+0.19)
      - mood match: intense (+0.12)
      - genre match: rock (+0.08)

#2  Gym Hero by Max Pulse
    Score: 0.84 / 1.00   [pop, intense]
    Why:
      - energy close to target: 0.93 vs 0.92 (+0.35)
      - acousticness close to target: 0.05 vs 0.08 (+0.24)
      - valence close to target: 0.77 vs 0.45 (+0.14)
      - mood match: intense (+0.12)

#3  Iron Requiem by Black Anvil
    Score: 0.74 / 1.00   [metal, aggressive]
    Why:
      - energy close to target: 0.97 vs 0.92 (+0.33)
      - acousticness close to target: 0.03 vs 0.08 (+0.24)
      - valence close to target: 0.28 vs 0.45 (+0.17)

#4  Pulse Cathedral by Hyperlane
    Score: 0.73 / 1.00   [edm, euphoric]
    Why:
      - energy close to target: 0.94 vs 0.92 (+0.34)
      - acousticness close to target: 0.04 vs 0.08 (+0.24)
      - valence close to target: 0.73 vs 0.45 (+0.14)

#5  Concrete Verses by Dre Cadence
    Score: 0.71 / 1.00   [hip hop, defiant]
    Why:
      - energy close to target: 0.68 vs 0.92 (+0.27)
      - acousticness close to target: 0.12 vs 0.08 (+0.24)
      - valence close to target: 0.45 vs 0.45 (+0.20)
================================================================
```

*Storm Runner* is the only rock song, so it wins easily at 0.99. The rest of the list is a mix of other loud songs, such as pop, metal and EDM. There is no second rock song to recommend, which shows how small the catalog is.

### Adversarial profiles

**Conflicting: Sad but Energetic**

```
================================================================
PROFILE: Conflicting: Sad but Energetic
classical / melancholy | energy 0.9 | valence 0.1 | acoustic 0.95
================================================================

#1  Adagio for Rain by Elena Voss
    Score: 0.71 / 1.00   [classical, melancholy]
    Why:
      - energy close to target: 0.15 vs 0.90 (+0.09)
      - acousticness close to target: 0.97 vs 0.95 (+0.24)
      - valence close to target: 0.22 vs 0.10 (+0.18)
      - mood match: melancholy (+0.12)
      - genre match: classical (+0.08)

#2  Iron Requiem by Black Anvil
    Score: 0.51 / 1.00   [metal, aggressive]
    Why:
      - energy close to target: 0.97 vs 0.90 (+0.33)
      - acousticness close to target: 0.03 vs 0.95 (+0.02)
      - valence close to target: 0.28 vs 0.10 (+0.16)

#3  Storm Runner by Voltline
    Score: 0.51 / 1.00   [rock, intense]
    Why:
      - energy close to target: 0.91 vs 0.90 (+0.35)
      - acousticness close to target: 0.10 vs 0.95 (+0.04)
      - valence close to target: 0.48 vs 0.10 (+0.12)

#4  Dust Road Home by Willow Creek
    Score: 0.50 / 1.00   [country, nostalgic]
    Why:
      - energy close to target: 0.52 vs 0.90 (+0.22)
      - acousticness close to target: 0.74 vs 0.95 (+0.20)
      - valence close to target: 0.66 vs 0.10 (+0.09)

#5  Night Drive Loop by Neon Echo
    Score: 0.49 / 1.00   [synthwave, moody]
    Why:
      - energy close to target: 0.75 vs 0.90 (+0.30)
      - acousticness close to target: 0.22 vs 0.95 (+0.07)
      - valence close to target: 0.49 vs 0.10 (+0.12)
================================================================
```

The system could not satisfy both halves, and it split the list. *Adagio for Rain* wins on genre, mood, acousticness and valence even though its energy (0.15) is far from the 0.9 target. Slots 2–5 are loud songs that match only the energy target (metal, rock) or nothing at all. The scores drop from 0.71 to about 0.5. Nothing in the catalog is both sad and energetic, so a weighted sum can only compromise.

**Unknown Genre and Mood**

```
================================================================
PROFILE: Unknown Genre and Mood
bossa nova / dreamy | energy 0.5 | valence 0.5 | acoustic 0.5
================================================================

#1  Velvet Hours by Marisol Kane
    Score: 0.72 / 1.00   [r&b, romantic]
    Why:
      - energy close to target: 0.49 vs 0.50 (+0.35)
      - acousticness close to target: 0.28 vs 0.50 (+0.20)
      - valence close to target: 0.62 vs 0.50 (+0.18)

#2  Midnight Coding by LoRoom
    Score: 0.71 / 1.00   [lofi, chill]
    Why:
      - energy close to target: 0.42 vs 0.50 (+0.32)
      - acousticness close to target: 0.71 vs 0.50 (+0.20)
      - valence close to target: 0.56 vs 0.50 (+0.19)

#3  Dust Road Home by Willow Creek
    Score: 0.70 / 1.00   [country, nostalgic]
    Why:
      - energy close to target: 0.52 vs 0.50 (+0.34)
      - acousticness close to target: 0.74 vs 0.50 (+0.19)
      - valence close to target: 0.66 vs 0.50 (+0.17)

#4  Focus Flow by LoRoom
    Score: 0.68 / 1.00   [lofi, focused]
    Why:
      - energy close to target: 0.40 vs 0.50 (+0.32)
      - acousticness close to target: 0.78 vs 0.50 (+0.18)
      - valence close to target: 0.59 vs 0.50 (+0.18)

#5  Island Sway by Sol Rivera
    Score: 0.67 / 1.00   [reggae, uplifting]
    Why:
      - energy close to target: 0.58 vs 0.50 (+0.32)
      - acousticness close to target: 0.31 vs 0.50 (+0.20)
      - valence close to target: 0.79 vs 0.50 (+0.14)
================================================================
```

With no genre or mood match possible and all targets at 0.5, the scores are almost tied (0.67–0.72). The top 5 spans r&b, lofi, country and reggae, so the ranking is close to arbitrary. The system returns confident-looking numbers when it actually has no signal.

**Extreme Targets**

```
================================================================
PROFILE: Extreme Targets
metal / peaceful | energy 0.0 | valence 1.0 | acoustic 0.0
================================================================

#1  Birchwood Lullaby by Moss & Ember
    Score: 0.52 / 1.00   [folk, peaceful]
    Why:
      - energy close to target: 0.24 vs 0.00 (+0.27)
      - acousticness close to target: 0.93 vs 0.00 (+0.02)
      - valence close to target: 0.58 vs 1.00 (+0.12)
      - mood match: peaceful (+0.12)

#2  Velvet Hours by Marisol Kane
    Score: 0.48 / 1.00   [r&b, romantic]
    Why:
      - energy close to target: 0.49 vs 0.00 (+0.18)
      - acousticness close to target: 0.28 vs 0.00 (+0.18)
      - valence close to target: 0.62 vs 1.00 (+0.12)

#3  Island Sway by Sol Rivera
    Score: 0.48 / 1.00   [reggae, uplifting]
    Why:
      - energy close to target: 0.58 vs 0.00 (+0.15)
      - acousticness close to target: 0.31 vs 0.00 (+0.17)
      - valence close to target: 0.79 vs 1.00 (+0.16)

#4  Sunrise City by Neon Echo
    Score: 0.44 / 1.00   [pop, happy]
    Why:
      - energy close to target: 0.82 vs 0.00 (+0.06)
      - acousticness close to target: 0.18 vs 0.00 (+0.21)
      - valence close to target: 0.84 vs 1.00 (+0.17)

#5  Concrete Verses by Dre Cadence
    Score: 0.42 / 1.00   [hip hop, defiant]
    Why:
      - energy close to target: 0.68 vs 0.00 (+0.11)
      - acousticness close to target: 0.12 vs 0.00 (+0.22)
      - valence close to target: 0.45 vs 1.00 (+0.09)
================================================================
```

A "metal, peaceful" listener with energy 0.0 gets a folk lullaby first. The only metal song (*Iron Requiem*) is missing from the top 5, because its energy (0.97) is the opposite of the target and the 0.08 genre bonus cannot make up for that. The best score is only 0.52, but the list still looks normal, because the system never says "nothing here fits".

### What these experiments show

- **Standard profiles work.** When the catalog has songs that fit, the top results match intuition.
- **Conflicting tastes get a compromise, not an answer.** The list is split between the label side (genre and mood) and the energy side.
- **No "nothing fits" signal.** Every profile gets five confident-looking results, even when the best score is 0.52 or the top five are nearly tied.
- **Low genre weight (0.08) has a cost.** A listener who cares mainly about genre can lose their only matching song to closer audio numbers.

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



