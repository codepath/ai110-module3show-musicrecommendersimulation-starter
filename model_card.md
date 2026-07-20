# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeMatch takes a listener's taste (genre, mood, energy, and whether they like acoustic sounds) and returns the top 5 songs from a small catalog that best match. It assumes the user can describe their taste in these four simple fields, and that those fields are typed correctly. This is a classroom project, not a real product. It's meant to teach how recommenders turn data into rankings, not to serve real listeners.

**Intended use:**
- Learning how a simple scoring-based recommender works
- Testing how changes to weights or inputs change the output
- Exploring bias and edge cases in a toy system

**Not intended for:**
- Real users picking real music
- Any catalog bigger or more diverse than this 18-song CSV
- Making decisions that matter (this system has known bugs and biases, see below)

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song starts at 0 points. If the song's genre matches what the user likes, it gets extra points. Same for mood. Then we look at energy: the closer the song's energy is to the user's target energy, the more points it gets, so a perfect match gets the most points and a far-off match gets none. Last, if the song's acoustic-ness fits whether the user likes acoustic music or not, it gets a small bonus. We add all of that up, sort every song from highest score to lowest, and hand back the top 5.

We also ran an experiment where we doubled the energy weight and cut the genre weight in half. That made energy matter a lot more than genre, and it visibly changed the rankings — songs that only matched on energy started beating songs that only matched on genre.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog is a small CSV with 18 songs. Each song has a genre, a mood, an energy value, a tempo, a valence score, a danceability score, and an acousticness score. There are 15 genres total, but most only have one song — only lofi has more than one (3 songs). Moods are just as spread out: 14 different moods across 18 songs. We didn't add or remove any songs. Because the catalog is so small and spread thin, a lot of real musical taste isn't represented well — there's no way to find "more songs like this one" if your favorite genre only has a single entry.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for listeners whose taste lines up with genres that have more than one song, like lofi. For our "Chill Lofi" test profile, the top 3 results were all real lofi/chill/low-energy songs, which matched what we'd expect a chill lofi fan to want. The energy scoring also works exactly as intended: when we compared a high-energy profile to a low-energy profile, the recommended songs were completely different and made sense (energetic pop and rock songs vs. quiet lofi and ambient songs). The explanations printed alongside each score (like "genre match" or "energy close to target") also make it easy to see why a song was recommended, which is a strength for a learning project like this.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system's catalog is heavily imbalanced: `lofi` has 3 songs while 14 other genres (including `classical`, `metal`, and `country`) have exactly 1 song each, yet genre match is worth the same fixed points regardless of how many candidates exist for that genre. As a result, a lofi listener gets 3 real songs to rank against each other and a genuinely differentiated top 5, while a metal or classical fan gets only one genre-matching song and the rest of their list is filled with fallback picks chosen almost entirely by energy closeness. The same pattern shows up with energy: songs cluster in a "low/chill" band (0.18–0.55) and a "high/intense" band (0.66–0.97), so users whose target energy lands in one of these dense bands are rewarded with many close matches, while users near the gap in between or at the extremes get comparatively weak, undifferentiated recommendations. In both cases the system never signals to the user that their taste is underserved — it confidently returns a ranked top 5 regardless of how few good matches actually exist. This means the recommender systematically favors "mainstream" tastes relative to this catalog and could quietly steer niche listeners toward songs that don't really match their preferences.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

**Core profiles** (`src/main.py`):
- **High-Energy Pop** — `genre: pop, mood: happy, energy: 0.8, likes_acoustic: False`
- **Chill Lofi** — `genre: lofi, mood: chill, energy: 0.4, likes_acoustic: True`
- **Deep Intense Rock** — `genre: rock, mood: intense, energy: 0.9, likes_acoustic: False`

**Adversarial / edge-case profiles**:
- **Conflicting energy/mood** — `genre: rock, mood: sad, energy: 0.9` (no song in the catalog has mood `sad`)
- **Nonexistent genre** — `genre: opera, mood: happy, energy: 0.5` (no song has genre `opera`)
- **Case mismatch** — `genre: Pop, mood: Happy, energy: 0.8` (same intent as High-Energy Pop, different capitalization)
- **Extreme out-of-range energy** — `genre: pop, mood: happy, energy: 5.0` (outside the valid 0–1 range)
- **Zero-signal profile** — `genre: zzz, mood: zzz, energy: 0.5` (both genre and mood are nonsense)
- **Missing `likes_acoustic`** — same as High-Energy Pop but the optional key is omitted
- **Missing `mood`** — required key omitted entirely

I looked at whether the top results actually matched the stated taste, whether swapping one field (energy, mood, genre, or case) changed the ranking in a way that made sense, and whether the system failed gracefully or silently on bad input.

### What surprised me

The biggest surprise was that a nonsensical mood (`sad`, which no song has) didn't change the ranking at all compared to a valid, matching mood — the scoring logic can't tell the difference between "this preference wasn't met" and "this preference doesn't exist in the data," so it produces a confident top 5 either way. I also didn't expect the case-sensitivity issue to be as impactful as it was: capitalizing "Pop" instead of "pop" cost a song 1.5 points and reshuffled the entire top 5, even though a human would consider those the same genre.

### Pairwise comparisons

- **High-Energy Pop vs. Chill Lofi**: Opposite energy targets (0.8 vs. 0.4) produce completely disjoint top-5 lists — `Sunrise City`/`Gym Hero` (high-energy pop tracks) vs. `Midnight Coding`/`Library Rain` (low-energy lofi tracks). This makes sense: the energy-gap term dominates once genre/mood don't overlap, so pulling the target energy down shifts the whole ranking toward mellower songs.
- **High-Energy Pop vs. Deep Intense Rock**: Both target high energy (0.8 vs. 0.9), so `Gym Hero` (pop/intense) shows up in both top 5s even though its genre matches neither user's stated genre. This is valid behavior — it shows the energy and mood terms alone are strong enough to surface a song across two different taste profiles when genre doesn't line up.
- **Chill Lofi vs. Deep Intense Rock**: Near-opposite energy targets (0.4 vs. 0.9) produce zero overlap between top-5 lists. This is the clearest confirmation that the energy-gap formula is doing its job — it correctly separates mellow and high-intensity songs.
- **Conflicting energy/mood ("rock"/"sad") vs. Deep Intense Rock ("rock"/"intense")**: Same genre and energy target, only the mood differs. Both rank `Storm Runner` (rock/intense) first with almost identical scores, because no song has mood `sad`, so that term contributes 0 in both cases. This exposes a real weakness: the system can't distinguish "your mood preference wasn't satisfied" from "your mood preference is impossible," so a clearly conflicting profile still gets a confident, seemingly reasonable answer.
- **Case Mismatch ("Pop"/"Happy") vs. High-Energy Pop ("pop"/"happy")**: Identical intent, different capitalization. `Sunrise City` should win by a wide margin in both, but the case-mismatched version loses the genre and mood bonuses entirely (exact string equality fails on `"Pop" != "pop"`), dropping its score from 7.96 to 2.96 and letting unrelated songs like `Concrete Crown` (hip-hop) creep into the top 3. This is not valid behavior — a real user typing "Pop" instead of "pop" shouldn't get worse recommendations.
- **Nonexistent genre ("opera") vs. Zero-signal ("zzz"/"zzz")**: Both have a genre with zero catalog matches, but "opera" keeps a valid mood (`happy`), while "zzz" has neither. As a result, the opera profile still surfaces mood-appropriate songs (`Rooftop Lights`, `Sunrise City`), while the zero-signal profile collapses to pure energy/acousticness ranking (`Open Road Memory`, `Midnight Coding`) with no clear connection to genre or mood. This makes sense given the additive scoring design, but it means an even mildly-wrong user input can produce a list with almost no interpretable rationale.
- **Missing `likes_acoustic` vs. High-Energy Pop**: Same top-3 order (`Sunrise City`, `Gym Hero`, `Rooftop Lights`), just with every score exactly 1.0 lower since the acoustic bonus is skipped entirely (guarded by the `"likes_acoustic" in user_prefs` check). This confirms the optional key is handled gracefully and, for these songs, doesn't change relative ranking — though it could tip closely-scored songs in a smaller gap.
- **Missing `mood`**: Crashes with `KeyError: 'mood'` instead of returning a ranked list. Compared to every other profile above (which all return *something*, right or wrong), this is the one case where the system fails loudly rather than silently — arguably safer than a wrong answer, but inconsistent with how every other missing/invalid field is handled.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. Make genre and mood matching case-insensitive and trim extra spaces, so typos like "Pop" vs "pop" don't tank a song's score.
2. Check that required fields (genre, mood, energy) exist before scoring, and give a clear error message instead of crashing with a `KeyError`.
3. Add a "low confidence" warning when very few songs are close to what the user asked for, instead of always confidently returning a top 5.
4. Grow the catalog so every genre and mood has more than one song, which would make recommendations for niche tastes much more meaningful.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this taught me that a recommender is really just a scoring rule plus a sort — there's no magic, just decisions about what to weight and by how much. The most interesting thing I found was that the system can't tell the difference between "no song matches your mood" and "your mood doesn't exist in our data" — it just confidently gives you its best guess either way. That made me realize real recommendation apps probably have the same blind spot, just hidden behind a much bigger catalog. It also made me think more about how a tiny bug, like comparing strings without matching case, can quietly change someone's whole set of recommendations without ever throwing an error.
