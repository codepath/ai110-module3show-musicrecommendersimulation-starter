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

Real-world recommendation systems combine content information about songs with behavioral signals such as plays, skips, likes, and playlists from many listeners. This simulation focuses on the content-based part: it compares a listener's stated taste profile with each song's attributes. It prioritizes genre and mood matches, then rewards songs whose energy is close to the listener's target and whose acousticness matches their preference. Each song receives a score, and the highest-scoring songs become the recommendations.

The simulation uses these features:

- `Song`:  `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
- `UserProfile`: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.

### Algorithm Recipe

For every song, the recommender starts at 0 points. It adds 3 points for a matching genre and 2 points for a matching mood. It then rewards energy closeness with `2 * (1 - abs(song_energy - target_energy))`, so a song whose energy is closer to the target earns more points. Finally, it adds 1 point when the song's acousticness fits whether the listener likes acoustic music. After scoring every song, it sorts the songs from highest score to lowest score and returns the top five.

### Potential Biases

This system may over-prioritize genre and miss a great song from a different genre that has the right mood or energy. It also relies on a small catalog and simple labels, so genres and moods that have fewer songs will be less likely to appear in recommendations. Because it does not use listening behavior such as skips or saves, it cannot learn when a listener's taste changes.


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

```
Loaded songs: 18

Top recommendations for High-Energy Pop
========================================
1. Sunrise City — Neon Echo
   Score: 7.96
   Reasons:
   - genre match (+3.0)
   - mood match (+2.0)
   - energy close to target (+1.96)
   - acousticness matches preference (+1.0)

2. Gym Hero — Max Pulse
   Score: 5.74
   Reasons:
   - genre match (+3.0)
   - energy close to target (+1.74)
   - acousticness matches preference (+1.0)

3. Rooftop Lights — Indigo Parade
   Score: 4.92
   Reasons:
   - mood match (+2.0)
   - energy close to target (+1.92)
   - acousticness matches preference (+1.0)

4. Concrete Crown — Rhythm District
   Score: 2.94
   Reasons:
   - energy close to target (+1.94)
   - acousticness matches preference (+1.0)

5. Night Drive Loop — Neon Echo
   Score: 2.90
   Reasons:
   - energy close to target (+1.90)
   - acousticness matches preference (+1.0)


Top recommendations for Chill Lofi
========================================
1. Midnight Coding — LoRoom
   Score: 7.96
   Reasons:
   - genre match (+3.0)
   - mood match (+2.0)
   - energy close to target (+1.96)
   - acousticness matches preference (+1.0)

2. Library Rain — Paper Lanterns
   Score: 7.90
   Reasons:
   - genre match (+3.0)
   - mood match (+2.0)
   - energy close to target (+1.90)
   - acousticness matches preference (+1.0)

3. Focus Flow — LoRoom
   Score: 6.00
   Reasons:
   - genre match (+3.0)
   - energy close to target (+2.00)
   - acousticness matches preference (+1.0)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 4.76
   Reasons:
   - mood match (+2.0)
   - energy close to target (+1.76)
   - acousticness matches preference (+1.0)

5. Coffee Shop Stories — Slow Stereo
   Score: 2.94
   Reasons:
   - energy close to target (+1.94)
   - acousticness matches preference (+1.0)


Top recommendations for Deep Intense Rock
========================================
1. Storm Runner — Voltline
   Score: 7.98
   Reasons:
   - genre match (+3.0)
   - mood match (+2.0)
   - energy close to target (+1.98)
   - acousticness matches preference (+1.0)

2. Gym Hero — Max Pulse
   Score: 4.94
   Reasons:
   - mood match (+2.0)
   - energy close to target (+1.94)
   - acousticness matches preference (+1.0)

3. Neon Kinetics — Signal Bloom
   Score: 2.98
   Reasons:
   - energy close to target (+1.98)
   - acousticness matches preference (+1.0)

4. Iron Horizon — Black Compass
   Score: 2.86
   Reasons:
   - energy close to target (+1.86)
   - acousticness matches preference (+1.0)

5. Concrete Crown — Rhythm District
   Score: 2.86
   Reasons:
   - energy close to target (+1.86)
   - acousticness matches preference (+1.0)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Adversarial / Edge Case Evaluation

To stress-test the scoring logic, we ran several "adversarial" user profiles designed to trigger conflicting preferences, invalid input, or degenerate matches. Each profile's raw terminal output is pasted below.

### Conflicting energy/mood

`{"genre": "rock", "mood": "sad", "energy": 0.9, "likes_acoustic": False}`

```
=== Conflicting energy/mood ===
prefs: {'genre': 'rock', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}
  Storm Runner (rock/intense) score=5.98 | genre match (+3.0); energy close to target (+1.98); acousticness matches preference (+1.0)
  Neon Kinetics (electronic/energetic) score=2.98 | energy close to target (+1.98); acousticness matches preference (+1.0)
  Gym Hero (pop/intense) score=2.94 | energy close to target (+1.94); acousticness matches preference (+1.0)
```

### Nonexistent genre

`{"genre": "opera", "mood": "happy", "energy": 0.5, "likes_acoustic": False}`

```
=== Nonexistent genre ===
prefs: {'genre': 'opera', 'mood': 'happy', 'energy': 0.5, 'likes_acoustic': False}
  Rooftop Lights (indie pop/happy) score=4.48 | mood match (+2.0); energy close to target (+1.48); acousticness matches preference (+1.0)
  Sunrise City (pop/happy) score=4.36 | mood match (+2.0); energy close to target (+1.36); acousticness matches preference (+1.0)
  Velvet Afterglow (r&b/romantic) score=2.90 | energy close to target (+1.90); acousticness matches preference (+1.0)
```

### Case mismatch

`{"genre": "Pop", "mood": "Happy", "energy": 0.8, "likes_acoustic": False}`

```
=== Case mismatch ===
prefs: {'genre': 'Pop', 'mood': 'Happy', 'energy': 0.8, 'likes_acoustic': False}
  Sunrise City (pop/happy) score=2.96 | energy close to target (+1.96); acousticness matches preference (+1.0)
  Concrete Crown (hip-hop/confident) score=2.94 | energy close to target (+1.94); acousticness matches preference (+1.0)
  Rooftop Lights (indie pop/happy) score=2.92 | energy close to target (+1.92); acousticness matches preference (+1.0)
```

### Extreme out-of-range energy

`{"genre": "pop", "mood": "happy", "energy": 5.0, "likes_acoustic": False}`

```
=== Extreme out-of-range energy ===
prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 5.0, 'likes_acoustic': False}
  Sunrise City (pop/happy) score=6.00 | genre match (+3.0); mood match (+2.0); energy close to target (+0.00); acousticness matches preference (+1.0)
  Gym Hero (pop/intense) score=4.00 | genre match (+3.0); energy close to target (+0.00); acousticness matches preference (+1.0)
  Rooftop Lights (indie pop/happy) score=3.00 | mood match (+2.0); energy close to target (+0.00); acousticness matches preference (+1.0)
```

### Zero-signal profile (all mismatched)

`{"genre": "zzz", "mood": "zzz", "energy": 0.5, "likes_acoustic": True}`

```
=== Zero-signal profile (all mismatched) ===
prefs: {'genre': 'zzz', 'mood': 'zzz', 'energy': 0.5, 'likes_acoustic': True}
  Open Road Memory (country/nostalgic) score=2.96 | energy close to target (+1.96); acousticness matches preference (+1.0)
  Midnight Coding (lofi/chill) score=2.84 | energy close to target (+1.84); acousticness matches preference (+1.0)
  Focus Flow (lofi/focused) score=2.80 | energy close to target (+1.80); acousticness matches preference (+1.0)
```

### Missing `likes_acoustic` key

`{"genre": "pop", "mood": "happy", "energy": 0.8}`

```
=== Missing likes_acoustic key ===
prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
  Sunrise City (pop/happy) score=6.96 | genre match (+3.0); mood match (+2.0); energy close to target (+1.96)
  Gym Hero (pop/intense) score=4.74 | genre match (+3.0); energy close to target (+1.74)
  Rooftop Lights (indie pop/happy) score=3.92 | mood match (+2.0); energy close to target (+1.92)
```

### Missing `mood` key (should crash)

`{"genre": "pop", "energy": 0.8, "likes_acoustic": False}`

```
=== Missing mood key (should crash) ===
prefs: {'genre': 'pop', 'energy': 0.8, 'likes_acoustic': False}
  CRASHED: KeyError: 'mood'
```

### Findings

- **Case sensitivity bug**: genre/mood comparisons are exact-string matches, so `"Pop"` fails to match `"pop"` even though it's clearly the same genre. This silently drops 5 points from a song that should be a perfect match.
- **No required-key validation**: omitting `genre`, `mood`, or `energy` crashes with an unhandled `KeyError` instead of a clear error message.
- **Silent degradation on typos/unknown values**: a nonexistent genre or a conflicting mood doesn't warn the user — it just quietly zeroes out that score component, which can produce recommendations that don't actually reflect the stated mood (e.g., the "sad" profile above still recommends an "intense" song).
- **No range clamping on `energy`**: values outside 0–1 are accepted without complaint; the internal `max(0.0, ...)` prevents a crash but there's no validation that the input is meaningful.

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

### Personal Reflection on the Engineering Process

My biggest learning moment was during the adversarial testing, when I fed the recommender a profile with a mood ("sad") that didn't exist anywhere in the dataset. I expected some kind of warning or a visibly worse result, but instead it confidently returned a normal-looking top 5 — it had no way to tell the difference between "this preference wasn't matched" and "this preference is impossible." That's when it clicked for me that a recommender's confidence and its correctness are two completely separate things, and nothing in the code was checking for that gap.

AI tools helped me move fast in two ways: generating a batch of edge-case profiles I wouldn't have thought to write myself (case mismatches, missing keys, out-of-range values), and quickly running experiments like the energy/genre weight shift and summarizing what changed. But I had to double-check almost every claimed "bug" by actually running the code and reading the real scores — for example, verifying with real terminal output that "Pop" vs "pop" really did cost a song 1.5 points, rather than trusting a plausible-sounding explanation. I also had to sanity-check the math myself when weights changed (making sure the energy term still stayed within a valid 0–4 range after doubling it) instead of assuming the AI's summary was airtight.

What surprised me most is how "smart" this system can feel despite being nothing more than adding up a few numbers and sorting them. Printing a plain-English reason next to each score (like "genre match (+3.0)") made the recommendations feel intentional and thoughtful, even though the underlying logic is just simple arithmetic on four fields. It made me realize that a lot of the "feel" of a recommendation system comes from how it explains itself, not just from how sophisticated the math actually is.

If I extended this project, I'd first fix the case-sensitivity bug and add validation for missing/invalid fields, since those are the easiest wins with the biggest impact on trust. Then I'd grow the catalog so niche genres aren't stuck with just one song, and add a genuine diversity mechanism (like avoiding two songs by the same artist in the top 5) instead of always returning the raw highest scores. Finally, I'd want to add real user feedback (likes/skips) so the system could start learning instead of just scoring against a fixed static profile every time.
