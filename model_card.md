# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a classroom simulation tool for understanding how content-based music recommendation works. It is intended for:

- Students learning how data attributes translate into ranked predictions
- Exploring how weight choices create or reinforce algorithmic bias
- Demonstrating the gap between simple rule-based systems and production-scale recommenders

**This model is not intended for real users or production deployment.** It has a tiny catalog, no user history, and no mechanism to learn or adapt over time.

---

## 3. How the Model Works

VibeFinder compares a user's taste profile to every song in the catalog and assigns each song a numeric score. Songs with higher scores are assumed to be better matches.

The scoring works like this:

1. **Genre match** is the most valuable signal. If the song's genre is exactly what the user listed as their favorite, the score jumps by 2 points. This reflects the idea that genre is the broadest filter people apply when choosing music.

2. **Mood match** adds 1 point. If the song's mood label matches the user's preferred mood, it gets a bonus. Because mood is more granular than genre, it earns half as many points.

3. **Energy proximity** adds a number between 0 and 1 depending on how close the song's energy level is to the user's target energy. A perfect energy match adds 1.0; a song that is completely opposite on the energy scale adds close to 0.

4. **Acoustic preference** adds a small bonus (0.5 or 0.3) if the song's acoustic character aligns with whether the user prefers acoustic or electronic sounds.

Songs are then sorted by their total score and the top five are returned along with the reason each one scored well.

---

## 4. Data

- **Catalog size:** 20 songs (10 original starter songs + 10 added during Phase 2)
- **Features per song:** genre, mood, energy (0–1), tempo BPM, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres represented:** pop, lofi, rock, ambient, synthwave, jazz, indie pop, metal, bossa nova, hip-hop, funk, country, edm, folk
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, peaceful, nostalgic, euphoric

**Gaps and limitations in the data:**

- The catalog skews toward Western popular music styles. Genres like K-pop, afrobeats, or classical are not present.
- All mood and genre labels are hand-assigned; they do not come from audio analysis.
- Ten songs (half the catalog) represent only three genres: pop, lofi, and rock. This imbalance means those genres will surface more often regardless of user preferences.

---

## 5. Strengths

- **Transparency:** Every recommendation comes with a plain-language explanation of exactly why that song scored high. There is no hidden signal.
- **Works well for mainstream profiles:** Profiles centered around pop/happy or lofi/chill consistently surface the most relevant songs because those genres have multiple representatives in the catalog.
- **Continuous energy scoring:** Unlike mood and genre (which are binary exact matches), energy is scored on a smooth scale so a song that is *close* to the target still earns partial credit rather than zero.
- **Predictable behavior:** Because the weights are fixed and simple, it is easy to reason about why any specific result appeared.

---

## 6. Limitations and Bias

**Filter bubble / genre dominance:** Genre carries a +2.0 bonus, which is double the mood bonus and up to twice the maximum energy bonus. This means a song with the right genre will almost always beat a song with perfect mood and energy alignment but a different genre. Users who love metal or bossa nova will always receive the same 1–2 songs at the top because those genres have only one representative each.

**Binary category matching:** Mood and genre are compared with exact string equality. "Indie pop" never matches "pop," and "euphoric" never matches "happy," even though a human listener would consider them closely related.

**No diversity enforcement:** The algorithm will repeat the same artist (e.g., Voltline appears twice in the rock catalog) without penalty. A real system would penalize repeated artists.

**Acoustic bias is weak:** The +0.3/+0.5 acoustic bonus is small enough that it rarely changes the rank order. Users who care deeply about whether a track is acoustic vs. electronic are not well served.

**No learning:** The model never updates from feedback. Skipping a recommended song has no effect on future recommendations.

---

## 7. Evaluation

Three distinct user profiles were tested during Phase 4:

**High-Energy Pop Fan** (genre=pop, mood=happy, energy=0.85)
- Top results: Sunrise City (#1, score 3.97), Gym Hero (#2, score 2.92)
- Both are pop tracks. "Sunrise City" hit genre + mood + close energy. "Gym Hero" matches genre + energy but has an intense mood. The genre bonus was strong enough to keep it in second place despite the mood mismatch.
- Surprising result: "Uptown Funk Revival" (funk/happy/0.87) ranked third purely on mood + energy — it had no genre match but still beat all non-pop non-happy tracks.

**Chill Lofi Listener** (genre=lofi, mood=chill, energy=0.38)
- Top results: Library Rain and Midnight Coding nearly tied at 3.97 and 3.96 respectively.
- After the two clear lofi/chill matches, the gap to third place (Focus Flow, 2.98) was large, and everything below that dropped below 1.0 score. The system correctly isolated the lofi niche.

**Deep Intense Rock** (genre=rock, mood=intense, energy=0.92)
- Top result: Storm Runner (3.99) — a near-perfect match.
- Second: Roaring Sunrise (rock/happy/0.80, score 2.88) — this was the weight-shift test. A rock-happy song outscored intense-metal and intense-hip-hop songs purely because of the genre bonus. This confirmed the dominance of the genre weight.

**Weight-shift experiment:** Halving genre weight (1.0) and doubling energy weight showed that Electronic Euphoria (edm, 0.93 energy) entered the rock profile's top 3. This demonstrated how much a single weight decision shapes the entire ranking.

---

## 8. Future Work

1. **Fuzzy genre and mood matching:** Build a small similarity map so "indie pop" earns partial genre credit against a "pop" profile, and "euphoric" earns partial credit against "happy."
2. **Diversity penalty:** If the same artist already appears in the top results, reduce the score of subsequent songs by that artist to encourage variety.
3. **Collaborative filtering layer:** Record which songs users skip or replay and use that history to adjust weights over time — moving from pure content-based to a hybrid approach.
4. **Tempo range preference:** Add `target_tempo_bpm` and `tempo_range` to UserProfile so the system can reward songs with a matching BPM, enabling more fine-grained energy differentiation (e.g., a slow sad song vs. a slow ambient song have very different feels despite similar energy scores).
5. **Larger and more diverse catalog:** Ten genres across 20 songs is too thin. A real deployment would need thousands of tracks per genre to avoid the filter bubble problem.

---

## 9. Personal Reflection

The most surprising thing about building VibeFinder was how quickly the weight choices overshadowed everything else. I spent time designing the scoring formula, but the moment I changed genre weight from 2.0 to 1.0, the entire ranked list shuffled — proving that *the weights are the model*, not the code structure around them.

Working on the bias analysis also made me rethink how I use Spotify. When the same two songs kept appearing at the top of every profile that included "rock," I realized that what feels like a sophisticated recommendation is often just the algorithm reflecting the composition of the catalog back at you. If there are only two rock songs available, a rock lover will only ever see those two, no matter how "smart" the rest of the logic is.

The biggest limitation I'd prioritize for improvement is the exact-string genre matching. Music genres exist on a spectrum and overlap heavily in real life. Teaching the algorithm to recognize that "indie pop" is closer to "pop" than it is to "metal" would make a bigger practical difference than any weight tuning.
