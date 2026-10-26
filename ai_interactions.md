# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add five advanced song attributes to the dataset and make the scoring use them. The agent had to change the data file, the loader, the scoring function and the demo profiles, then check the result and update the docs.

**Prompts used:**

> Add Advanced Song Features. Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes. In ai_interactions.md, document the agentic workflow: the example prompt(s) you used, a summary of the changes the AI generated, and your manual verification notes.

**What did the agent generate or change?**

- `data/songs.csv`: added 5 columns to all 18 songs: `popularity`, `release_decade`, `mood_tags`, `instrumentalness`, `explicit`. A script appended them so the original values were not retyped.
- `src/recommender.py`:
  - `load_songs` now converts the new columns (ints, a float, a yes/no flag and a list of tags).
  - `score_song` was restructured. It collects each feature as a (weight, similarity) pair, and divides by the weights in use. A feature only counts when the user sets its preference.
  - New weights: popularity 0.10, decade 0.10, mood tags 0.15, instrumentalness 0.10, clean lyrics 0.05.
  - The `Song` dataclass got the new fields with defaults, so the existing tests still build.
- `src/main.py`: added four demo profiles that use the new features (Mainstream Hits, Nostalgic Throwback, Instrumental Study Session, Clean Workout).
- `README.md` and `model_card.md`: documented the new features, weights and the fact that the new values are made up.
- Commands run: `python -m src.main`, `python3 -m pytest`, and a script that compares rankings with and without the new preferences.

**What did you verify or fix manually?**

- **Old behavior unchanged.** I saved the earlier output of the six original profiles and compared. The new output starts with exactly the same text, so adding the features did not change those results. The 2 tests still pass.
- **The new features change rankings.** I ran each new profile with and without its advanced preferences:
  - Mainstream Hits: *Gym Hero* (popularity 88) moved above *Rooftop Lights* (74).
  - Nostalgic Throwback: *Island Sway* entered the top 5. *Dust Road Home* stayed first.
  - Instrumental Study Session: *Birchwood Lullaby* replaced *Dust Road Home*, helped by the "cozy" tag.
  - Clean Workout: *Iron Requiem* (explicit) dropped in score, from 0.74 to 0.68.
- **A weakness I found.** `avoid_explicit` only nudges. *Iron Requiem*, an explicit song, still ranks 4th for a user who wants clean music. A real filter would remove it. I documented this in the README instead of hiding it.
- **The data is invented.** The agent made up the popularity, decade, tag and instrumentalness values. They look plausible, but they are not real data. The model card says so.
- **Score points.** Because scores are divided by the weights in use, the "+0.xx" reasons are scaled and add up to the final score. I checked this by reading the printed reasons for *Storm Runner*.
- **Still for me to check:** whether the weights feel right. They are my judgment and I only tested a few profiles.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

**Strategy**, in a simple data-driven form. Each scoring mode is a table of weights. One shared scorer reads whichever table it is given, so modes can be swapped without changing the scoring code.

**How did AI help you brainstorm or implement it?**

I gave the AI `recommender.py` and asked for a modular way to add several scoring modes. It suggested three options:

1. **`if/elif` on the mode inside `score_song`.** Quick, but every new mode means editing the function and the code gets messy.
2. **One scoring function per mode** (the textbook Strategy pattern). Clean, but each function would repeat the same similarity math, and a bug fix would need to be made in each one.
3. **One shared scorer plus a weight table per mode.** The modes differ only in their weights, so only the weights need to be swapped.

We picked option 3. The AI pointed out that the modes only differ in weights, so separate functions would just be copy and paste. It also suggested keeping the default mode identical to the old recipe. That let me prove nothing broke by comparing old and new output.

Where I had to think for myself: the AI proposed the weights, but I checked that they made sense for each mode. I checked the results with `--compare` and with the tests.

**How does the pattern appear in your final code?**

- `SCORING_MODES` and `BALANCED` at the top of `src/recommender.py` hold the weight tables. A new mode is one new entry.
- `score_song(user_prefs, song, mode)` looks up the table and raises `ValueError` for an unknown mode.
- `recommend_songs(..., mode)` passes the mode through.
- `src/main.py` has the `--mode` and `--compare` switches.
- `tests/test_scoring_modes.py` has 9 tests. They use four tiny songs, each built to win under one mode. I also broke the code on purpose (made every mode use the balanced weights) and confirmed 3 tests failed, so the tests really do check the modes.

**Branch note.** I did the work on a new branch, `experiment/scoring-modes`, so `main` stayed safe. The default `balanced` output is byte-for-byte identical to before. I have not merged the branch.
