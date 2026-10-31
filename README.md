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

In general, recommender systems use a combination of content-based and collaborative filtering. Collaborative filtering relies on user behavior for similar users to predict which songs you are likely to have interest in. This is known as a clustering approach in machine learning. Content-based filtering evaluates the metadata and other attributes and features for a song to determine if it will interest you. Collaborative filtering does the heavy lifting without prior knowledge of your behavior while content-based is more personalized once specific data points are available for you.

This recommender is content-based. It scores each song on its own by how well it fits the user's taste, then ranks all the scores and returns the best few. Energy is scored by closeness to the target, not by being higher or lower, and mood outweighs genre because mood better reflects what the listener wants right now. Acousticness is scored as a smaller preference signal: listeners who like acoustic music are rewarded for acoustic songs, and everyone else is rewarded for less acoustic ones.

- **Song features:** `energy`, `mood`, `genre`, and `acousticness` are scored. `tempo_bpm`, `valence`, and `danceability` are stored for later.
- **UserProfile:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`
- **Score:** `0.40 * energy_score + 0.25 * mood_match + 0.20 * genre_match + 0.15 * acoustic_score`, for a maximum of 1.0, where:
  - `energy_score = 1 - |song.energy - target_energy|`
  - `mood_match` and `genre_match` are 1 for a match and 0 for a miss
  - `acoustic_score = song.acousticness` if `likes_acoustic` is true, otherwise `1 - song.acousticness`
- **Ranking:** score every song, sort high to low, and return the top `k` with the reasons for each score

Note that this system will prioritize mood over genre, energy is heavily weighted because it is a numeric feature and it uses exact matches for labels ignoring synonyms.

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

If running on Windows using PowerShell, use the below command instead.

```powershell
python src/main.py
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

The below is a sample command line example of the recommender's output on a Windows machine.

```
============================================================
TOP RECOMMENDATIONS
Profile: lofi | chill | energy 0.40 | likes acoustic
============================================================

1. Library Rain - Paper Lanterns
   Score: 0.96 / 1.00
   Why:
     * energy 0.35 vs target 0.40 (+0.38)
     * mood match (+0.25)
     * genre match (+0.20)
     * acoustic fit 0.86 (+0.13)
------------------------------------------------------------

2. Midnight Coding - LoRoom
   Score: 0.95 / 1.00
   Why:
     * energy 0.42 vs target 0.40 (+0.39)
     * mood match (+0.25)
     * genre match (+0.20)
     * acoustic fit 0.71 (+0.11)
------------------------------------------------------------

3. Spacewalk Thoughts - Orbit Bloom
   Score: 0.74 / 1.00
   Why:
     * energy 0.28 vs target 0.40 (+0.35)
     * mood match (+0.25)
     * acoustic fit 0.92 (+0.14)
------------------------------------------------------------

4. Focus Flow - LoRoom
   Score: 0.72 / 1.00
   Why:
     * energy 0.40 vs target 0.40 (+0.40)
     * genre match (+0.20)
     * acoustic fit 0.78 (+0.12)
------------------------------------------------------------

5. Porch Light Promise - Willow Creek
   Score: 0.53 / 1.00
   Why:
     * energy 0.38 vs target 0.40 (+0.39)
     * acoustic fit 0.91 (+0.14)
------------------------------------------------------------
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

Expected biases and limitations of this scoring rule:

- **Mood can crowd out genre.** Because mood (0.25) outweighs genre (0.20), a song with the right mood but the wrong genre can beat a song in the user's favorite genre. For a `lofi`/`chill` listener, Spacewalk Thoughts (ambient, chill) can outrank Focus Flow (lofi, focused).
- **Exact-match labels are all or nothing.** Near-synonyms such as `chill`/`relaxed` or `pop`/`indie pop` get zero credit, so good songs can be missed on a technicality.
- **Energy carries the most weight.** At 0.40, and because energy values are bunched together, the ranking can drift toward songs with the right energy but little else in common with the user's taste.
- **The acoustic preference is binary.** A user with `likes_acoustic = false` is rewarded for non-acoustic songs even if they simply have no opinion, which quietly penalizes folk, jazz and classical.
- **The catalog is tiny and uneven.** Most genres have a single song, while `lofi` and `chill` appear three times each, so lofi/chill listeners get more variety than everyone else.
- **It can create a filter bubble.** The system only scores similarity to a stated profile, so it never suggests anything outside the user's stated tastes, and it does not understand lyrics or language.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



