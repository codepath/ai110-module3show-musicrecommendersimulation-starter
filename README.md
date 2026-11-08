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

Real-world recommendation engines process massive pipelines of user behavior, social interactions, and multi-layered content metadata to predict user preferences in real time. While production systems like Spotify use complex matrices, collaborative filtering, and deep learning to predict what millions of listeners want next, my version will prioritize structural consistency, targeted mood filtering, and strict numerical proximity. By assigning a dominant weight to foundational genres, utilizing active mood tags as cross-genre bridges, and applying a Gaussian bell-curve penalty to fine-tune raw audio vectors like energy and valence, this implementation focuses on delivering high-fidelity, context-aware sonic recommendations without requiring massive user historical tracking data.

### Data Flow

```
INPUT                        PROCESS (the loop)                 OUTPUT (the ranking)
─────                        ──────────────────                 ────────────────────
User prefs (dict)  ──┐
                     ├──►  for each song in the catalog:  ──►  sort by score (high → low)
data/songs.csv ──────┘       score_song(prefs, song)            ties broken by id
  via load_songs()           → (score, reasons)                 keep the top k
                                                                → (song, score, explanation)
```

- `load_songs()` reads the CSV and converts number columns from text to `float`/`int`.
- `score_song()` judges **one** song at a time and does not compare it with the others.
- `recommend_songs()` runs the loop, sorts the results and returns the top `k`.

### Algorithm Recipe

**Song features used:** `genre`, `mood`, `energy`, `valence`, `danceability`, `acousticness`

**User profile stores:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`, and optionally `target_valence` and `target_danceability`. If an optional target is missing, its rule is skipped.

**Scoring rules for each song:**

| # | Rule | Points | Max |
|---|---|---|---|
| 1 | **Genre:** exact match, ignoring case | +2.0 | 2.0 |
|   | Partial match: one genre name contains the other (e.g. "indie pop" and "pop") | +1.0 | |
| 2 | **Mood:** exact match, ignoring case | +1.0 | 1.0 |
| 3 | **Energy closeness:** `1 − |target_energy − energy|` | 0 to 1 | 1.0 |
| 4 | **Valence closeness:** `1 − |target_valence − valence|` (if given) | 0 to 1 | 1.0 |
| 5 | **Danceability closeness:** `1 − |target_danceability − danceability|` (if given) | 0 to 1 | 1.0 |
| 6 | **Acoustic fit:** `acousticness` if `likes_acoustic`, otherwise `1 − acousticness` | 0 to 1 | 1.0 |

**Maximum score: 7.0.** The two label matches (genre and mood) are worth up to 3 points and the four number features up to 4. A song with the right labels that sounds wrong can therefore still lose to a better-sounding song.

The number features reward songs that are *close* to the target, not songs with the highest values. A user who wants energy 0.70 is not shown the most intense track just because it has the most energy.

**Why genre counts twice as much as mood:** energy, valence and danceability already partly capture mood (a "happy" song tends to have high valence and energy), so a large mood bonus would count it twice. No other feature captures genre.

**Explanations:** every rule that adds points also adds a reason, such as `"genre match: pop (+2.0)"` or `"energy 0.82 close to target 0.70 (+0.88)"`. The reasons are joined with `"; "` into the explanation shown to the user.

**Ranking:** score all 20 songs, sort from highest to lowest (ties broken by `id`), and return the top `k`.

**Left out on purpose:**
- **Tempo:** it mostly repeats what energy measures, and BPM would need converting to a 0–1 scale.
- **Artist:** in a 20-song catalog it would just repeat the two artists who have two songs each.

### Potential Biases I Expect

- **Genre over-weighting:** a genre match (+2.0) can outweigh a better overall fit. For the "Upbeat Pop Listener", *Gym Hero* (pop, intense) is expected to rank just above *Rooftop Lights* (indie pop, happy), even though the happier song fits the request better.
- **Uneven catalog:** lofi has 3 songs, while most genres have only 1. Lofi fans get several genre matches, while a fan of a genre that isn't in the catalog (e.g. k-pop) can never earn genre points.
- **Strict labels:** genre and mood are matched as text. Related labels such as "sad" and "melancholy", or "r&b" and "soul", earn nothing. Each song also has only one mood, chosen by whoever labeled the data.
- **Yes/no acoustic preference:** `likes_acoustic = False` pushes down every acoustic-heavy genre (classical, folk, jazz, lofi), even for a user who would enjoy one occasionally.
- **No variety control:** the system can recommend several very similar songs, and nothing encourages variety or discovery outside the user's stated taste.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

You are an expert Python developer. Help me write the data structures for a music recommendation system in `src/models.py`. 

Please create two clean, typed classes (or dataclasses):
1. `Song`: 
   - Attributes: song_id (str), title (str), artist (str), genre (str), mood (str), energy (float), and valence (float).
   - Ensure numerical properties are validated to fall between 0.0 and 1.0.

2. `UserProfile`:
   - Attributes: user_id (str), preferred_genre (str), preferred_mood (str), target_energy (float), and target_valence (float).

  Provide clean, modular code with type hinting and short docstrings.

- What information does your `UserProfile` store
You are an expert algorithm engineer. Help me write the `compute_score(song, user_profile)` function inside `src/recommender.py`.

Please implement this exact scoring rule:
- Base Score starts at 0.0.
- Categorical Rules (Exact String Matching): 
  * If song.genre matches user_profile.preferred_genre, add a weight of 2.0.
  * If song.mood matches user_profile.preferred_mood, add a weight of 1.5.
- Numerical Rules (Gaussian/Bell Curve Proximity):
  * Do not use a simple linear penalty. Instead, implement a Gaussian function to reward closeness.
  * Formula for feature score: math.exp(-((song_value - target_value) ** 2) / (2 * (0.2 ** 2)))
  * Calculate this Gaussian score for 'energy' (weighted by 1.0) and 'valence' (weighted by 1.0).
- Return the final calculated float score. Ensure math libraries are imported and edge cases are handled.

- How does your `Recommender` compute a score for each song
You are an expert software architect. Help me implement the `recommend_songs(user_profile, catalog, top_k=5)` function in `src/recommender.py`.

Please implement the following ranking pipeline logic:
1. Accept the user_profile and a list of all Song objects (the catalog).
2. Calculate the score for every song using our `compute_score` rule.
3. Sort the catalog in descending order based on the calculated scores.
4. Implement a diversity filter: Ensure the same artist cannot occupy more than 2 slots in the final output list.
5. Slice and return the top_k results.
6. Provide an automated string output for each recommendation explaining why it was chosen (e.g., "Matches your chill mood and indie genre preference!").

- How do you choose which songs to recommend
Based on the code models, scoring rules, and ranking logic we just discussed, please write a comprehensive, ready-to-paste markdown text block for the "How The System Works" section of my project's README.md file. 

Address these bullet points explicitly in clear, professional language:
- What features does each Song use in your system
- What information does your UserProfile store
- How does your Recommender compute a score for each song
- How do you choose which songs to recommend

Include a clean ASCII text diagram or markdown table illustrating the scoring pipeline (Data Inputs -> Scoring Rule -> Ranking Rule -> Final Top 5 Playlist) to make it scannable and easy to read.

You can include a simple diagram or bullet list if helpful.

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


Rank	Song	Expected	Actual
1	Sunrise City	6.65	6.65 ✅
2	Gym Hero	5.61	5.61 ✅
3	Rooftop Lights	5.56	5.56 ✅
4	Paper Crowns	3.63	3.63 ✅
5	Neon Cathedral	3.51	3.51 ✅
Why this order makes sense for pop/happy

#1 Sunrise City is the only song in the catalog that is both pop and happy, and it's close on every number feature, so it should win clearly. It does, by more than a point.
The top 3 are exactly the songs that match on genre or mood. The two pop songs are Sunrise City and Gym Hero; the two happy songs are Sunrise City and Rooftop Lights. All three outrank every song with no label match.
#4 and #5 match neither label but are upbeat, danceable and not acoustic, which is still a reasonable fit. The big drop from 5.56 to 3.63 marks where the label matches end.
The bottom of the list makes sense too. The lowest score is Winter Letters (classical, melancholy, very acoustic) at 1.31, nearly the opposite of this profile.
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



