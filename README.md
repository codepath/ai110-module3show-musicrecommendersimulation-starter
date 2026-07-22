# 🎵 Music Recommender Simulation — VibeFinder 1.0

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version is a **content-based** recommender: it never looks at what other users liked, only at the attributes of each song compared to one user's stated taste profile. It loads a small CSV catalog, scores every song against a user's preferences using a transparent, weighted point system, and returns the top K songs along with a plain-language explanation of why each one scored the way it did.

---

## How The System Works

**Real-world systems** like Spotify or YouTube typically blend two approaches. **Collaborative filtering** predicts what you'll like based on the behavior of *other* users with similar tastes (e.g., "people who liked these songs also liked this one"), using signals like plays, skips, likes, and playlist co-occurrence. **Content-based filtering** (what this project implements) instead looks at the *attributes* of the items themselves — genre, tempo, mood, energy — and matches them directly against a user's stated or inferred preferences. Real platforms combine both, plus contextual signals (time of day, device, session history), to build a full recommendation.

This simulation intentionally prioritizes **transparency over sophistication**: every recommendation comes with a human-readable list of reasons, so you can see exactly which rule fired and how many points it contributed.

**Song features used:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness (see data/songs.csv).

**UserProfile stores:** favorite_genre, favorite_mood, target_energy, and likes_acoustic (a boolean for whether the user prefers acoustic-leaning or produced/electronic-leaning songs).

**Algorithm Recipe (scoring rule), applied per song:**

- +2.0 if the song's genre matches the user's favorite genre
- +1.0 if the song's mood matches the user's favorite mood
- Up to +2.0 for energy similarity, computed as 2.0 * (1 - |song energy - target energy|) — this rewards songs whose energy is *close* to the target rather than simply high or low
- +1.0 if the song's acousticness agrees with the user's likes_acoustic preference (acoustic songs, acousticness of 0.5 or higher, for users who like acoustic; produced/electronic songs, acousticness below 0.5, for users who don't)

**Ranking rule:** the Recommender and recommend_songs functions score *every* song in the catalog with the rule above, then sort the full list from highest to lowest score and return the top k. A **scoring rule** judges one song in isolation; a separate **ranking rule** is needed because recommending is fundamentally a *comparison* across the whole catalog — you can't know if a song is "good" for a user until you've scored its competitors too.

**Potential bias:** because genre and mood are binary "hit or miss" bonuses while energy is continuous, a song that matches genre and mood but is *wildly* off on energy can still outrank a song that's a near-perfect energy match but misses genre/mood. This is visible in the "Edge Case" profile in the Sample Output below.

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

You can add more tests in tests/test_recommender.py.

---

## Sample Recommendation Output

Output of running python -m src.main against the expanded 18-song catalog, using four profiles (three "normal" tastes plus one adversarial edge case):

```
Loaded songs: 18

=== High-Energy Pop ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

1. Sunrise City by Neon Echo - Score: 5.96
   Because: genre match: pop (+2.0); mood match: happy (+1.0); energy similarity: target 0.8, song 0.82 (+1.96); acoustic preference match: acousticness 0.18 (+1.0)
2. Gym Hero by Max Pulse - Score: 4.74
   Because: genre match: pop (+2.0); energy similarity: target 0.8, song 0.93 (+1.74); acoustic preference match: acousticness 0.05 (+1.0)
3. Rooftop Lights by Indigo Parade - Score: 3.92
   Because: mood match: happy (+1.0); energy similarity: target 0.8, song 0.76 (+1.92); acoustic preference match: acousticness 0.35 (+1.0)
4. Night Drive Loop by Neon Echo - Score: 2.90
   Because: energy similarity: target 0.8, song 0.75 (+1.90); acoustic preference match: acousticness 0.22 (+1.0)
5. Storm Runner by Voltline - Score: 2.78
   Because: energy similarity: target 0.8, song 0.91 (+1.78); acoustic preference match: acousticness 0.1 (+1.0)

=== Chill Lofi ===
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}

1. Library Rain by Paper Lanterns - Score: 6.00
   Because: genre match: lofi (+2.0); mood match: chill (+1.0); energy similarity: target 0.35, song 0.35 (+2.00); acoustic preference match: acousticness 0.86 (+1.0)
2. Midnight Coding by LoRoom - Score: 5.86
   Because: genre match: lofi (+2.0); mood match: chill (+1.0); energy similarity: target 0.35, song 0.42 (+1.86); acoustic preference match: acousticness 0.71 (+1.0)
3. Focus Flow by LoRoom - Score: 4.90
   Because: genre match: lofi (+2.0); energy similarity: target 0.35, song 0.4 (+1.90); acoustic preference match: acousticness 0.78 (+1.0)
4. Spacewalk Thoughts by Orbit Bloom - Score: 3.86
   Because: mood match: chill (+1.0); energy similarity: target 0.35, song 0.28 (+1.86); acoustic preference match: acousticness 0.92 (+1.0)
5. Coffee Shop Stories by Slow Stereo - Score: 2.96
   Because: energy similarity: target 0.35, song 0.37 (+1.96); acoustic preference match: acousticness 0.89 (+1.0)

=== Deep Intense Rock ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

1. Storm Runner by Voltline - Score: 5.98
   Because: genre match: rock (+2.0); mood match: intense (+1.0); energy similarity: target 0.9, song 0.91 (+1.98); acoustic preference match: acousticness 0.1 (+1.0)
2. Gym Hero by Max Pulse - Score: 3.94
   Because: mood match: intense (+1.0); energy similarity: target 0.9, song 0.93 (+1.94); acoustic preference match: acousticness 0.05 (+1.0)
3. Neon Temple by Kilowatt - Score: 2.90
   Because: energy similarity: target 0.9, song 0.95 (+1.90); acoustic preference match: acousticness 0.03 (+1.0)
4. Iron Cathedral by Grim Choir - Score: 2.86
   Because: energy similarity: target 0.9, song 0.97 (+1.86); acoustic preference match: acousticness 0.05 (+1.0)
5. Sunrise City by Neon Echo - Score: 2.84
   Because: energy similarity: target 0.9, song 0.82 (+1.84); acoustic preference match: acousticness 0.18 (+1.0)

=== Edge Case: Energetic but Sad ===
User profile: {'genre': 'blues', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}

1. Heartbreak Hotel Redux by Velvet Ashes - Score: 4.80
   Because: genre match: blues (+2.0); mood match: sad (+1.0); energy similarity: target 0.9, song 0.3 (+0.80); acoustic preference match: acousticness 0.55 (+1.0)
2. Midnight Coding by LoRoom - Score: 2.04
   Because: energy similarity: target 0.9, song 0.42 (+1.04); acoustic preference match: acousticness 0.71 (+1.0)
3. Focus Flow by LoRoom - Score: 2.00
   Because: energy similarity: target 0.9, song 0.4 (+1.00); acoustic preference match: acousticness 0.78 (+1.0)
4. Storm Runner by Voltline - Score: 1.98
   Because: energy similarity: target 0.9, song 0.91 (+1.98)
5. Gym Hero by Max Pulse - Score: 1.94
   Because: energy similarity: target 0.9, song 0.93 (+1.94)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Weight shift experiment:** genre weight halved (2.0 → 1.0), energy-similarity weight doubled (max 2.0 → max 4.0), tested on the "High-Energy Pop" profile (genre=pop, mood=happy, energy=0.8).

Original recipe top 5: Sunrise City, Gym Hero, Rooftop Lights, Night Drive Loop, Storm Runner

Weight-shifted top 5: Sunrise City, Rooftop Lights, Gym Hero, Night Drive Loop, Storm Runner

*Rooftop Lights* (indie pop, energy 0.76 — no genre match) swapped ahead of *Gym Hero* (pop, energy 0.93 — genre match) once energy similarity was weighted more heavily than genre. This confirms the recipe is sensitive to relative weights: raising the energy weight lets a close energy match outrank a genre match, which could be desirable (energy "feel" matters more than genre label) or undesirable (genre is a stronger taste signal than a single number) depending on what a real product wants to optimize for.

**Profile stress test:** running the four profiles in src/main.py (High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial Energetic-but-Sad edge case) showed the recommender behaves reasonably for "coherent" profiles but produces a lopsided result for the edge case — see Limitations below.

---

## Limitations and Risks

- The catalog is tiny (18 songs across 15 genres), so there usually isn't more than one or two strong candidates per genre — the recommender looks confident, but it is really just sorting a very small pool.
- It only understands the numbers and labels in the CSV; it has no idea what a song actually sounds like, its lyrics, or its cultural context.
- Genre and mood are binary "hit or miss" bonuses while energy is continuous, so — as shown in the "Edge Case" profile in Sample Output — a song that matches genre and mood but is very far off on energy can still outrank a song with no genre/mood match but a near-perfect energy fit. A user with contradictory preferences (e.g., wanting "sad" + high energy) gets a recommendation that satisfies the labels but not the underlying vibe.
- Because content-based filtering only compares a song to a fixed profile, it will keep recommending the same handful of "safe" songs for a stable profile and can create a filter bubble — it never suggests something outside the stated genre/mood to help the user discover new taste, the way collaborative filtering might.

You will go deeper on this in your model card.

---

## Reflection

Read and complete model_card.md:

[**Model Card**](model_card.md)

Building this simulation made it concrete how much a "recommendation" really is just arithmetic dressed up in a friendly list: every ranking is the result of a handful of weighted rules applied consistently to rows in a spreadsheet. What surprised me is how quickly a system this simple starts to *feel* personal — the moment it prints "Because: genre match, mood match, energy similarity" next to a song title, it reads as insight, even though it's the same three if statements running on every row.

The bias question got a lot more concrete once I ran the adversarial "Energetic but Sad" profile: the system happily recommended a slow, mellow blues song to a user who explicitly wanted high energy, purely because genre and mood matched and energy didn't get enough relative weight to override that. In a real product this is exactly how a recommender can quietly ignore what a user is actually asking for while still looking confident. It also made clear how a small, non-diverse catalog (mostly pop/lofi in the starter data) can bias every profile's top results toward whatever genre is over-represented, regardless of how good the scoring math is.



