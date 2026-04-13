# Reflection: Music Recommender Simulation

## Profile Comparisons

### High-Energy Pop Fan vs. Chill Lofi Listener

These two profiles are essentially opposites on every axis — genre, mood, and energy — and the recommender reflected that perfectly. The pop fan's list was dominated by uptempo tracks with happy moods, while the lofi listener's list clustered around quiet, mellow songs. The gap between first place and third place was much larger for the lofi listener (~1.0 score gap) than for the pop fan, which suggests that "lofi/chill" is a tighter niche in the dataset — once you leave those two songs behind, nothing else fits closely.

### Chill Lofi Listener vs. Deep Intense Rock

These profiles share an interesting property: both have a clear, distinct genre in the catalog. The lofi listener's top two results (Library Rain and Midnight Coding) were nearly tied. The rock profile's top result (Storm Runner) was nearly perfect, but the second result was a *happy* rock song, not an intense one. This shows how the genre bonus wins even when the mood is wrong — a rock-happy song outscored an intense-metal song because genre weighs twice as much as mood. For the lofi listener, both lofi songs happened to also match the mood, so the pattern was less visible.

### High-Energy Pop Fan vs. Deep Intense Rock

Both profiles wanted high energy, but the rest of their preferences diverged completely. The pop fan's top five were dominated by cheerful, danceable songs; the rock fan's top five were loud and aggressive. Despite sharing a high target energy, they shared zero songs in their top five. This makes sense — energy proximity alone only adds up to 1.0 point, while a genre match is worth 2.0. Energy is a supporting signal, not the primary filter.

---

## What Changed When I Ran the Weight-Shift Experiment

When I halved the genre weight (from 2.0 to 1.0) and doubled the energy weight (from max 1.0 to max 2.0), the rock profile's top five changed significantly: Electronic Euphoria (edm, 0.93 energy) entered the top three, even though its genre is edm. This was surprising at first, but it makes total sense — when energy matters twice as much as genre, songs that are close in energy can beat songs that share a genre but have very different energy levels.

The takeaway: the weights are the model. Changing one number reshapes the entire ranking. This is exactly why real recommender systems tune their weights carefully using user feedback data rather than picking them by intuition.

---

## How AI Tools Helped — and When I Had to Double-Check

AI tools were most useful in three places: generating the initial expanded song catalog, suggesting the energy-proximity formula (`1.0 - abs(target - song.energy)`), and helping phrase the model card sections in plain language. In all three cases the output was a good starting point but needed judgment applied on top of it.

The place where I had to be most careful was the song catalog. The AI-generated songs had plausible titles and artists but the numeric values (energy, valence, danceability) needed to be checked manually against what those genres actually feel like. For example, a generated "country" song had an energy of 0.87, which felt too high for the genre — I kept it but noted it as an edge of the data. I also had to verify that genre and mood labels were self-consistent, because the AI sometimes assigned "happy" to a song in a genre that typically skews melancholic.

The second area requiring double-checking was the scoring weights. AI tools can suggest weights but can't tell you if they *feel* right for your catalog. The only way to validate them was to run the code and see whether the top-5 results matched musical intuition — which they mostly did, but the edge-case profile revealed that genre dominance can produce clearly wrong results that no amount of prompt engineering would have flagged in advance.

---

## What I Learned

Building this simulation taught me that the hardest part of a recommender is not the code — it's deciding what to measure and how much each measurement should matter. Getting the scoring formula running took an afternoon; understanding why the results were right or wrong took much longer.

I was also surprised by how quickly filter bubbles appeared in a 20-song catalog. With only two lofi songs available, a lofi listener's experience is essentially fixed from the start. Scaling the catalog is not just a performance problem — it is a fairness problem. Every genre that is under-represented will produce a worse experience for users who prefer it.
