# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

**Comparing a result to my own musical intuition:** For the **High-Energy Pop** profile (`genre=pop, mood=happy, energy=0.9`), the top result was:

```
1. Sunrise City by Neon Echo - Score: 4.42
   - genre match (pop) (+2.0)
   - mood match (happy) (+1.0)
   - energy closeness (+0.92)
   - non-acoustic preference match (+0.5)
```

I asked my AI coding assistant to explain, from the current weights in `recommender.py`, exactly why this song beat everything else. My prompt was: *"Based on the weights in `_score_components` in `recommender.py`, explain why Sunrise City ranked #1 for the High-Energy Pop profile instead of Gym Hero (also pop, also non-acoustic)."*

The answer: `Sunrise City` is `genre="pop"` and `mood="happy"`, so it earns both the full **+2.0 genre bonus** and the full **+1.0 mood bonus** — the only song in the catalog that hits both for this profile. Its `energy` (0.82) is close to the target (0.9), earning **+0.92** of the possible 1.0. It's also non-acoustic (`acousticness=0.18 < 0.4`), matching the implied `likes_acoustic=False` default, for **+0.5**. Total: `2.0 + 1.0 + 0.92 + 0.5 = 4.42`. `Gym Hero` is pop but `mood="intense"`, not `"happy"`, so it loses the full 1.0 mood point — that gap alone is why it lands second at 3.47 instead of first, even though its own energy (0.93) is technically closer to 0.9 than Sunrise City's.

This matches my intuition: if I personally wanted a happy, high-energy pop song, `Sunrise City` is exactly the kind of song I'd expect to see recommended first — it's the only song that satisfies both stated preferences (genre and mood) at once, and the system correctly rewards that over a song that only satisfies one.

---

## 6. Limitations and Bias 

**The genre weight can make the same song dominate every list for that genre.** `Neon Pulse Overdrive` (the catalog's only `edm` song) ranked #1 for both the "Out-of-Range Energy" and "Contradictory Acoustic Preference" adversarial profiles in Section 7 — different moods, energies, and acoustic preferences, same winner — purely because it's the sole song that can claim the **+2.0 genre bonus** for `edm`. With only 18 songs and mostly one song per genre, the +2.0 genre weight is large enough relative to the rest of the recipe (max 2.5 combined from mood/energy/acoustic) that whichever song owns a genre will usually win any profile requesting that genre, regardless of how well its mood or energy actually fits. This is both a strength (it makes genre-consistent recommendations very reliable) and a bias risk: a bigger, more varied catalog with several songs per genre would be needed before genre weighting stops effectively picking a single "default song" per genre.

**The "energy gap" calculation quietly assumes genre and energy are correlated, which creates a filter bubble for users whose taste doesn't fit that assumption.** I asked my AI coding assistant to check `recommender.py` and `data/songs.csv` together for hidden biases, and it flagged that every "chill" genre in the catalog (`lofi`, `ambient`, `jazz`, `folk`, `classical`, `blues`) has energy between 0.20-0.42, while every "upbeat" genre (`pop`, `rock`, `synthwave`, `indie pop`, `metal`, `hip-hop`, `edm`) sits between 0.75-0.97 — there is no low-energy rock song or high-energy lofi song anywhere in the data. Because of this, a user who wants, say, high-energy lofi can never score well on both `genre` and `energy` at once: no matter how the weights are tuned, the recipe will always force a tradeoff between the two for that listener, while a user whose taste happens to match the dataset's built-in genre/energy correlation gets full credit on both. This isn't a bug in the scoring formula itself, but a bias baked into the catalog that the formula has no way to detect or correct for — it silently underserves any "genre-atypical" listener (e.g., someone who likes energetic lofi or mellow rock) in favor of listeners whose preferences already match the dataset's assumptions.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

I tested three everyday profiles (defined in `src/main.py`'s `PROFILES` dict) and four adversarial/edge-case profiles (`ADVERSARIAL_PROFILES`) designed to try to "trick" the scoring logic. All output below is real terminal output from `python -m src.main`.

**What surprised me overall:** I expected a bad or nonsensical input (like `energy=1.5`, which is outside the 0-1 scale every song uses) to break the system or produce garbage. It didn't — the math just degrades gracefully. I was also surprised that the system never seems to *notice* when a profile contradicts itself (like wanting acoustic songs but also wanting EDM, which is never acoustic) — it doesn't detect the contradiction, it just scores each attribute separately and lets the fixed weights decide the winner. The biggest surprise, though, was how often the exact same one or two songs (`Gym Hero`, `Neon Pulse Overdrive`) kept reappearing across completely different profiles — explained in the comparisons below.

### Everyday profiles

**High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`)
```
1. Sunrise City by Neon Echo - Score: 4.42
   - genre match (pop) (+2.0)
   - mood match (happy) (+1.0)
   - energy closeness (+0.92)
   - non-acoustic preference match (+0.5)

2. Gym Hero by Max Pulse - Score: 3.47
   - genre match (pop) (+2.0)
   - energy closeness (+0.97)
   - non-acoustic preference match (+0.5)

3. Rooftop Lights by Indigo Parade - Score: 2.36
   - mood match (happy) (+1.0)
   - energy closeness (+0.86)
   - non-acoustic preference match (+0.5)

4. Storm Runner by Voltline - Score: 1.49
   - energy closeness (+0.99)
   - non-acoustic preference match (+0.5)

5. Neon Pulse Overdrive by Kilowatt - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)
```

**Chill Lofi** (`genre=lofi, mood=chill, energy=0.35`)
```
1. Library Rain by Paper Lanterns - Score: 4.50
   - genre match (lofi) (+2.0)
   - mood match (chill) (+1.0)
   - energy closeness (+1.00)
   - acoustic preference match (+0.5)

2. Midnight Coding by LoRoom - Score: 4.43
   - genre match (lofi) (+2.0)
   - mood match (chill) (+1.0)
   - energy closeness (+0.93)
   - acoustic preference match (+0.5)

3. Focus Flow by LoRoom - Score: 3.45
   - genre match (lofi) (+2.0)
   - energy closeness (+0.95)
   - acoustic preference match (+0.5)

4. Spacewalk Thoughts by Orbit Bloom - Score: 2.43
   - mood match (chill) (+1.0)
   - energy closeness (+0.93)
   - acoustic preference match (+0.5)

5. Coffee Shop Stories by Slow Stereo - Score: 1.48
   - energy closeness (+0.98)
   - acoustic preference match (+0.5)
```

**Deep Intense Rock** (`genre=rock, mood=intense, energy=0.9`)
```
1. Storm Runner by Voltline - Score: 4.49
   - genre match (rock) (+2.0)
   - mood match (intense) (+1.0)
   - energy closeness (+0.99)
   - non-acoustic preference match (+0.5)

2. Gym Hero by Max Pulse - Score: 2.47
   - mood match (intense) (+1.0)
   - energy closeness (+0.97)
   - non-acoustic preference match (+0.5)

3. Neon Pulse Overdrive by Kilowatt - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)

4. Block Party Anthem by MC Tempo - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)

5. Iron Cathedral by Grim Choir - Score: 1.43
   - energy closeness (+0.93)
   - non-acoustic preference match (+0.5)
```

All three matched intuition: the song sharing both genre and mood with the profile always lands in first place, and the ranking decays sensibly as fewer attributes match.

### Adversarial / edge-case profiles

**Conflicting Signals (Energetic + Sad)** (`genre=blues, mood=sad, energy=0.9`) — blues is normally a low-energy genre in this catalog, and "sad" doesn't exactly match any `mood` value (the closest is `melancholic`).
```
1. Rainy Window Blues by Delta Hollow - Score: 2.40
   - genre match (blues) (+2.0)
   - energy closeness (+0.40)

2. Storm Runner by Voltline - Score: 1.49
   - energy closeness (+0.99)
   - non-acoustic preference match (+0.5)

3. Gym Hero by Max Pulse - Score: 1.47
   - energy closeness (+0.97)
   - non-acoustic preference match (+0.5)

4. Neon Pulse Overdrive by Kilowatt - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)

5. Block Party Anthem by MC Tempo - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)
```
Because `mood` matching is an exact string comparison, "sad" never matches "melancholic" even though they're the same idea — the only blues song in the catalog still wins on genre alone, but gets zero mood credit and a weak energy score since it's actually a slow song. This exposes a real limitation: the system has no concept of synonyms or mood similarity.

**Genre Not In Catalog** (`genre=country, mood=happy, energy=0.5`)
```
1. Rooftop Lights by Indigo Parade - Score: 2.24
   - mood match (happy) (+1.0)
   - energy closeness (+0.74)
   - non-acoustic preference match (+0.5)

2. Sunrise City by Neon Echo - Score: 2.18
   - mood match (happy) (+1.0)
   - energy closeness (+0.68)
   - non-acoustic preference match (+0.5)

3. Velvet Nights by Sable & Vine - Score: 1.45
   - energy closeness (+0.95)
   - non-acoustic preference match (+0.5)

4. Night Drive Loop by Neon Echo - Score: 1.25
   - energy closeness (+0.75)
   - non-acoustic preference match (+0.5)

5. Block Party Anthem by MC Tempo - Score: 1.15
   - energy closeness (+0.65)
   - non-acoustic preference match (+0.5)
```
No crash and no empty list — the system gracefully falls back to ranking by mood/energy/acoustic alone, which is the correct behavior for a genre with zero catalog matches.

**Out-of-Range Energy** (`genre=edm, mood=triumphant, energy=1.5`, outside the catalog's 0-1 scale)
```
1. Neon Pulse Overdrive by Kilowatt - Score: 3.95
   - genre match (edm) (+2.0)
   - mood match (triumphant) (+1.0)
   - energy closeness (+0.45)
   - non-acoustic preference match (+0.5)

2. Iron Cathedral by Grim Choir - Score: 0.97
   - energy closeness (+0.47)
   - non-acoustic preference match (+0.5)

3. Gym Hero by Max Pulse - Score: 0.93
   - energy closeness (+0.43)
   - non-acoustic preference match (+0.5)

4. Storm Runner by Voltline - Score: 0.91
   - energy closeness (+0.41)
   - non-acoustic preference match (+0.5)

5. Block Party Anthem by MC Tempo - Score: 0.85
   - energy closeness (+0.35)
   - non-acoustic preference match (+0.5)
```
The genre+mood match still wins comfortably even though its own energy is far from 1.5. This surprised me: because `energy` closeness is uncapped on the low end, songs with very low energy (nowhere in this top 5) would score *negative* points from that component instead of erroring out — the formula degrades gracefully rather than breaking, but it also silently accepts nonsensical input (`energy=1.5` on a 0-1 scale) with no validation or warning.

**Contradictory Acoustic Preference** (`genre=edm, mood=triumphant, energy=0.9`, but `likes_acoustic=True` even though EDM is definitionally non-acoustic)
```
1. Neon Pulse Overdrive by Kilowatt - Score: 3.95
   - genre match (edm) (+2.0)
   - mood match (triumphant) (+1.0)
   - energy closeness (+0.95)

2. Midnight Coding by LoRoom - Score: 1.02
   - energy closeness (+0.52)
   - acoustic preference match (+0.5)

3. Focus Flow by LoRoom - Score: 1.00
   - energy closeness (+0.50)
   - acoustic preference match (+0.5)

4. Storm Runner by Voltline - Score: 0.99
   - energy closeness (+0.99)

5. Dust Road Home by Wilder Pines - Score: 0.98
   - energy closeness (+0.48)
   - acoustic preference match (+0.5)
```
The genre/mood match wins even though it gets zero acoustic credit, since 2.0 + 1.0 comfortably outweighs the 0.5 acoustic bonus. The system doesn't "notice" the contradiction in the user's own stated preferences (an EDM fan who claims to like acoustic music) — it just scores each attribute independently and lets the weights resolve the conflict, which happens to produce a sensible top pick here but wouldn't necessarily always do so with a different weight balance.

### Comparing profiles to each other (plain language)

**High-Energy Pop vs. Chill Lofi** — these two flip almost everything: high energy vs. low energy, upbeat vs. relaxed genre, non-acoustic vs. acoustic. And the results flip right along with them — High-Energy Pop's top picks are loud, danceable pop songs, while Chill Lofi's top picks are quiet, acoustic-leaning lofi tracks. That makes sense: two people who want opposite things should get opposite recommendations, and they do.

**High-Energy Pop vs. Deep Intense Rock** — both ask for the same energy level (0.9) but a different genre and mood (`happy pop` vs. `intense rock`). Both profiles' #1 picks are genre-and-mood perfect matches (`Sunrise City`, `Storm Runner`), which makes sense — matching two things instead of one always wins. But look at the #2 spot in both lists: it's `Gym Hero` both times. That's the surprising part, explained below.

**Chill Lofi vs. Deep Intense Rock** — opposite in almost every way (calm/acoustic lofi vs. loud/aggressive rock), and the recommendations are opposite too — no song appears in both top 5 lists. This is the cleanest, most reassuring comparison: two very different listeners get two completely different sets of songs.

**Out-of-Range Energy vs. Contradictory Acoustic Preference** — both profiles ask for the same genre and mood (`edm`, `triumphant`), so it's no surprise that the exact same song, `Neon Pulse Overdrive`, wins #1 in both. What's interesting is *why* the two scores differ slightly (3.95 in one, 3.95 in the other, but for different reasons underneath): one profile's unrealistic energy target (1.5) shaves points off the energy component, while the other profile's contradictory "I like acoustic music" preference simply forfeits the whole 0.5 acoustic bonus (since EDM is never acoustic). Different flaws in the user's request, same underlying winner — a good sign that genre+mood dominance is consistent no matter which other input is "broken."

**Conflicting Signals vs. Genre Not In Catalog** — both are "broken" requests, but in different ways: one asks for a mood word (`sad`) that doesn't exist in the data, the other asks for a genre (`country`) that doesn't exist at all. When the genre doesn't exist, the system has *nothing* to lean on except mood/energy/acoustic, so the results feel weaker/more generic (nothing scores above 2.24). When the genre exists but the mood doesn't match, the system still leans hard on that one genre match — showing that a missing genre hurts the recommendations far more than a missing mood, which lines up with genre being weighted twice as heavily.

**Why does "Gym Hero" keep showing up when someone just wants "Happy Pop"?** In plain terms: `Gym Hero` is a pop song, and its intensity/energy level happens to be very close to whatever "high energy" a user asks for — so it checks two of the system's boxes (genre + energy) really well. But `Gym Hero`'s actual mood is tagged `intense`, not `happy` — it's a gym workout anthem, not a feel-good song. The system doesn't listen to the song or understand what "happy" really sounds like; it just adds up points for each box that's checked, and getting genre + energy right (2.0 + up to 1.0 = up to 3.0 points) is worth more than getting mood right alone (1.0 point). So a song that's "close enough" on two out of three things can beat, or nearly beat, a song that's a better emotional fit but only matches on one. To a non-programmer: it's like a matchmaking app that scores you highly with someone because you both like the same restaurants and live close by, even though your personalities don't actually get along — the app is weighing the wrong things more heavily than the thing that actually matters most to a happy match.

**Takeaway:** the scoring logic never crashed or returned nonsense, but exact-string matching (no synonyms/fuzzy matching) and the lack of input validation on out-of-range values are the two clearest weaknesses this evaluation surfaced.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
