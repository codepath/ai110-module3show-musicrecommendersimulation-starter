# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add advanced song features to the recommender. The agent had to add 5 or more new attributes to the data, make the scoring use them, and write up the workflow here. It did the whole thing in several steps on its own: read the code, edit the data and logic, run it, test it and document it.

**Prompts used:**

> Add Advanced Song Features. Introduce 5 or more complex attributes to our dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both `data/songs.csv` and the scoring logic in `src/recommender.py` so scoring accounts for the new attributes. In `ai_interactions.md`, document the agentic workflow: the example prompt(s) you used, a summary of the changes the AI generated, and your manual verification notes.

**What did the agent generate or change?**

*Data: `data/songs.csv`.* Five new columns on all 20 songs:

| Column | Type | Example |
|---|---|---|
| `popularity` | 0 to 100 | 85 |
| `release_decade` | year | 2020 |
| `mood_tags` | 2 to 3 tags joined with `\|` | `uplifting\|bright\|energetic` |
| `language` | text | `english`, `spanish`, `instrumental` |
| `instrumentalness` | 0.0 to 1.0 | 0.02 |

The original ten columns were not changed.

*Scoring: `src/recommender.py`.*

- `load_songs` reads the new columns. It turns `mood_tags` into a list.
- `Song` and `UserProfile` got matching optional fields with default values. This keeps old code and the existing tests working.
- New function `_advanced_points` scores the new features:
  - **Mood tags:** up to +1.0, based on the share of the user's tags the song has.
  - **Popularity:** up to +0.5 for being close on the 0 to 100 scale.
  - **Decade:** up to +0.5. The points reach 0 when the songs are 30 or more years apart.
  - **Language:** +0.5 for an exact match, ignoring capital letters.
  - **Instrumentalness:** up to +0.5 for being close on the 0 to 1 scale.
- New function `max_score` returns the highest possible score for a user. It is 4.0 for a basic profile. It grows by the points of each advanced preference the user gives, up to 7.0.
- The advanced features only count when the user gives that preference. So the original nine profiles score exactly as before.

*Runner and tests.*

- `src/main.py` prints each profile's own maximum score (for example `5.92 / 6.00`). It shows the advanced preferences when a profile has them. It has four new profiles: Nostalgic 90s Listener, Mainstream Hit Seeker, Spanish-Language Night Out and Instrumental Study Session.
- `tests/test_recommender.py` has 8 new tests. They cover each new feature, skipping songs that lack a value, the score ceiling, and reading the new columns.

**What did you verify or fix manually?**

Checks that were run:

- **No regressions.** I saved the output of the original nine profiles before the change. After the change, the output was byte-for-byte identical.
- **Original data untouched.** The first ten columns of all 20 rows match the version in git.
- **Score bounds.** I scored 129,600 combinations of unusual inputs against all 20 songs. The inputs included out-of-range popularity, years and instrumentalness, empty or mixed-case text, and a language that doesn't exist. No score went below 0 or above that profile's `max_score`.
- **Perfect match.** For every song, a profile copied from that song scored exactly its `max_score`.
- **Tests.** All 10 tests pass: the 2 original ones and the 8 new ones.
- **Display bug avoided.** `main.py` splits the reasons on `"; "`. The mood-tag reason therefore lists tags with commas, so each reason stays on one line in the terminal.
- **Listening check.** The advanced profiles gave results that fit: Dusty Porch Swing first for the nostalgic 90s listener, and Fuego en la Noche (the only Spanish song) first for the Spanish-language profile.

Things the agent could not check, which I should look at by hand:

- **The new data is made up.** The songs and artists are fictional, so the popularity, decade, tags, language and instrumentalness values were assigned by the agent. They are plausible, but they do not come from real streaming data.
- **The extra weights are guesses.** I have not tested whether 1.0 for tags and 0.5 for the others is the right balance.
- **Docs.** The README and model card describe the three-part score. They need a short update for the new features.
- **My own listening check.** The four advanced profiles should be judged by my own ear.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

A lightweight **Strategy pattern**. A ranking strategy is a small object that says how much genre, mood and energy are worth. The scorer takes a strategy as an input. The user picks the strategy by name.

There are three strategies. Each one's weights add up to 4.0, so scores stay on the same scale.

| Mode | Genre | Mood | Energy | Meaning |
|---|---|---|---|---|
| `genre-first` | 2.0 | 1.0 | 1.0 | Staying in your favorite genre matters most. |
| `mood-first` | 1.0 | 2.0 | 1.0 | Matching your mood matters most. |
| `energy-focused` | 1.0 | 1.0 | 2.0 | Matching your energy matters most. This is the default. |

**How did AI help you brainstorm or implement it?**

*Prompt used:*

> Build two or more different ranking strategies (e.g., "Genre-First," "Mood-First," or "Energy-Focused") so a user can switch between modes in `main.py`. Attach `recommender.py` and use your AI coding assistant's chat to brainstorm a design pattern (like a simple "Strategy" pattern) that keeps your code modular. In your `ai_interactions.md`, document the chosen design pattern and how AI contributed to brainstorming it. Consider prototyping the second mode on its own branch (`git checkout -b experiment/mood-first`) so your working version stays safe while you try the new one.

*Options the AI laid out before writing code:*

1. **`if mode == ...` branches inside `score_song`.** Quick to write. But every new mode adds more branches to one function, and the tests get harder.
2. **A subclass for each mode.** Flexible. But it is a lot of code when the modes only differ by weights.
3. **A frozen `RankingStrategy` object holding the weights, passed into the scorer.** The scoring steps are written once. A new mode is one new object. Callers pick it by name.

The AI recommended option 3 because the three modes only differ in emphasis. If a later mode needs different logic (for example, re-ranking for variety), it can get its own scoring method behind the same interface.

*What the AI did next:*

- Wrote the `RankingStrategy` class, the three strategies and a `get_strategy` lookup.
- Passed `strategy` through `score_song`, `max_score`, `recommend_songs` and the `Recommender` class. The default is `energy-focused`, so old callers behave as before.
- Added a `--mode` option and a `--profile` option to `main.py`.
- Wrote 6 new tests.
- Prototyped it on a separate branch, `experiment/mood-first`, as suggested.

**How does the pattern appear in your final code?**

- **`src/recommender.py`:**
  - `RankingStrategy` is the strategy class.
  - `GENRE_FIRST`, `MOOD_FIRST` and `ENERGY_FOCUSED` are the three strategies.
  - `STRATEGIES` is a lookup by key, and `get_strategy()` reads a name.
  - `score_song(prefs, song, strategy)` is the single shared scorer.
- **`src/main.py`:** `python3 -m src.main --mode mood-first` runs one mode. `--mode all` runs all three for each profile. `--profile rock` runs only profiles whose name contains "rock". With no flags, the output is the same as before.

**What did you verify or fix manually?**

Checks that were run:

- **Nothing changed by default.** The output of all 13 profiles with no flags is byte-for-byte identical to the output before this change.
- **Same scale in every mode.** Every strategy's weights add up to 4.0. Across all 13 profiles and 3 modes, no top-5 score went below 0 or above that profile's `max_score`.
- **The modes really differ.** The #1 song changes for two profiles:
  - Genre-Only Trap: Genre-First picks Iron Verdict (loud metal). The other two modes pick Spacewalk Thoughts (quiet ambient).
  - Classical + Angry: Genre-First picks Rainfall Nocturne (quiet classical). The other two modes pick Iron Verdict.
- **Mood-First helps the Gym Hero problem.** For the High-Energy Pop profile, Rooftop Lights (happy) now ranks above Gym Hero (intense).
- **Tests.** All 16 tests pass: the 10 from before and 6 new ones.

Things still to check by hand:

- **The modes agree more than they differ.** For most profiles, all three modes pick the same #1 song. The modes mainly change the lower ranks and the conflicting profiles. That may be right, but I should decide if it is enough variety.
- **Merging.** The work is on `experiment/mood-first`. I have to decide whether to merge it back or drop it.

---

## Diversity Penalty

> Document the prompt you wrote and what the AI did with it.

**The rule I wanted**

Stop the top results from filling up with one artist or one genre. If a song's artist (or genre) is already in the list, lower that song's score.

**Prompt used:**

> Add a "Diversity Penalty" to `src/recommender.py` so the top results don't repeat the same artist or genre.
>
> Rule: build the top-k list one song at a time. Before each pick, look at every song not yet picked. Subtract 0.75 from its score for each already-picked song by the same artist. Subtract 0.25 for each already-picked song in the same genre. The penalty stacks, so a third song by one artist loses 1.5. Never let a score drop below 0. Pick the song with the highest adjusted score. If two songs tie, keep the one that ranked higher before any penalty.
>
> Requirements:
> - Make it opt-in. With no penalty, results and scores must stay exactly as they are today.
> - Keep the penalty values in a small config object, not scattered numbers.
> - Add a line to each penalized song's "Reasons" that says why it lost points, so scores stay explainable.
> - Add a `--diverse` flag to `src/main.py`.
> - Add tests for: repeat artist, repeat genre, stacking, the zero floor, ties, and the `Recommender` class.
> - Check that scores stay between 0 and `max_score`.

**What did the agent generate or change?**

- `src/recommender.py`:
  - `DiversityPenalty` is a small config class with `artist_penalty` (0.75) and `genre_penalty` (0.25). `DEFAULT_DIVERSITY` holds those defaults.
  - `_pick_diverse` does the one-at-a-time picking. Ties go to the song that ranked higher before any penalty.
  - `recommend_songs` and the `Recommender` class take an optional `diversity` argument. The default is `None`, which means off.
  - A penalized song gets an extra reason, for example `diversity penalty: artist LoRoom already picked 1x, genre lofi already picked 2x (-1.25)`.
- `src/main.py`: a `--diverse` flag. When it is on, the output shows the penalty values.
- `tests/test_recommender.py`: 8 new tests.
- `README.md`: a short note on the flag.

**What did you verify or fix manually?**

Checks that were run:

- **Off by default.** With no flag, the output of all 13 profiles is byte-for-byte identical to before.
- **It does what the rule says.** With the penalty on, 5 of the 13 profiles change. For example:
  - Chill Lofi no longer has two LoRoom songs. Focus Flow drops out and Wildflower Road comes in.
  - Case Mismatch no longer has two Neon Echo songs. Night Drive Loop drops out.
  - Mainstream Hit Seeker and High-Energy Pop swap Gym Hero and Rooftop Lights, because Gym Hero shares the pop genre with #1.
- **Bounds.** With the penalty on, no top-5 score went below 0 or above the profile's `max_score`.
- **A test was wrong, not the code.** My first stacking test failed because I added up the scores wrong. I worked out the numbers by hand and fixed the test. The code was right. The fixed test now tells a stacking penalty apart from a flat one.
- **Tests.** All 24 tests pass: the 16 from before and 8 new ones.

Things to look at by hand:

- **It is a nudge, not a cap.** A song that matches strongly can still survive the penalty. The Instrumental Study Session profile still returns two LoRoom songs and three lofi songs, because those songs score much higher than the rest. That may be right for someone who asked for lofi.
- **The genre penalty can work against the user.** A listener who asks for lofi is penalized for getting several lofi songs. That is why the genre penalty (0.25) is smaller than the artist penalty (0.75).
- **The values are guesses.** I have not tested whether 0.75 and 0.25 are the right numbers.

---

## Formatted Table Output

> Document the prompt you wrote and what the AI did with it.

**The goal**

Make the terminal output easier to read. Show the top results in a table. Each row must include the reasons for the score.

**Prompt used:**

> Suggest a way to make the terminal output of `src/main.py` easier to read. Use a library like `tabulate`, or simple ASCII formatting. Show the top recommendations as a table.
>
> The table must include the "reasons" for each score. Do not drop them to make the table fit. Put the title, artist, score and reasons in the table.
>
> Requirements:
> - Tell me the options and your pick before you write code.
> - Long reasons must wrap inside the table. Fit the terminal width.
> - Show each song's score out of its maximum. The maximum changes with the profile.
> - Add a one-line summary under the table.
> - Keep the current layout as the default. Add a flag for the table.
> - Add tests. Check the table lines all have the same width.

**What did the agent suggest?**

| Option | Good | Not so good |
|---|---|---|
| `tabulate` library | One line of code. Handles multi-line cells. | It is not installed and not in `requirements.txt`. It adds a dependency. |
| `pandas` `to_string` | `pandas` is already in `requirements.txt`. | Heavy for a simple table. Does not wrap long text. |
| A small ASCII table function | No new dependency. I control the wrapping. | I have to write and test it. |

The agent picked the ASCII function. The reasons are long, multi-line text, and wrapping them to fit the terminal is the main need. Writing it by hand keeps setup the same.

**What did the agent generate or change?**

- New file `src/table.py` with `render_table(headers, rows, aligns, max_width)`:
  - Cells can have several lines.
  - Only the Reasons column shrinks to fit the width. Its text wraps onto more lines. Wrapped bullet lines get a hanging indent.
  - The width comes from the terminal. It falls back to 100 when output is piped.
- `src/main.py`: a `--table` flag. The table has the columns `#`, `Song` (title and artist), `Score` (for example `3.84/4.00`) and `Reasons`. A one-line summary follows: top pick, score range and number of songs and artists.
- `tests/test_table.py`: 5 new tests.
- `README.md`: a short section with a sample.

**What did you verify or fix manually?**

Checks that were run:

- **Nothing changed by default.** The output with no flags is byte-for-byte identical to before. So is the output with `--diverse --mode all`.
- **Reasons are never dropped.** Every reason line from the list layout appears in the table. This includes the long mood-tag, popularity and decade lines, and the diversity penalty line.
- **Fits the terminal.** With all profiles and modes, the widest table line was 80 at 80 columns and 100 at 100 columns.
- **Tests.** All 29 tests pass: the 24 from before and 5 new ones.

Things to look at by hand:

- **Very narrow terminals.** Below about 66 columns the table cannot shrink further. The `Song` column does not wrap. At 60 columns the widest line was 66.
- **Table is not the default.** I kept the list layout as the default so the sample output in the README and model card stays correct. Making the table the default is a small change, but those samples would then need regenerating.
- **How it looks.** I checked the layout by reading the output. I should look at it in my own terminal.
