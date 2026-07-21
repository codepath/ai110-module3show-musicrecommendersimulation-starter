# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch takes a simple taste profile and predicts which songs in a small catalog a person would probably like.

It's built for learning, not for real listeners. It's meant to show how a basic recommender works step by step.

**Good for:**
- Learning how recommenders turn preferences into scores
- Testing "what if" user profiles and seeing how the ranking changes
- Classroom demos and small experiments

**Not good for:**
- Real music apps with real users
- Any catalog bigger than a handful of songs (it doesn't scale)
- Making decisions that affect real people, like what gets promoted or paid out to artists

It assumes the user already knows their favorite genre, mood, and energy level, and that these preferences don't change over time. Real listeners rarely fit that neatly.

---

## 3. How the Model Works  

Every song has a genre, a mood, an energy level, and how acoustic it sounds.

Every user has a favorite genre, a favorite mood, a target energy level, and whether they like acoustic songs.

VibeMatch goes through every song one at a time and hands out points:
- Same genre as the user? +1.5 points
- Same mood as the user? +2 points
- Close energy level to what the user wants? Up to +4 points, more points the closer it is
- Acoustic-ness matches what the user likes? +1 point

Then it adds up the points for each song, sorts every song from highest score to lowest, and shows the top 5.

I started with genre worth +3 and energy worth up to +2. I flipped that on purpose, cutting genre in half and doubling energy, to see if energy-based matches would do a better job than genre alone. It helped a little, but it didn't fix everything — see Section 6.

---

## 4. Data  

The catalog has 18 songs, stored in `data/songs.csv`.

Each song has 9 fields: title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

I started with 10 songs and added 8 more, on purpose picking genres and moods that weren't covered yet, like classical, hip hop, metal, reggae, country, R&B, and techno.

Even after adding more, most genres and moods only have 1 song each. Only `lofi` (3 songs) and `chill` mood (3 songs) have more than two.

Things missing entirely: lyrics, language, artist popularity, release year, and any real listening history. The dataset is also all made up — it's not real streaming data, just numbers I assigned by hand.

---

## 5. Strengths  

It works best for users whose favorite genre already has more than one song in the catalog, like `lofi`. Their top results actually feel like a real playlist.

The energy-closeness math works the way you'd expect: songs with energy close to the target always score higher than songs far from it, and the gap gets bigger the further off a song is.

When genre, mood, and energy all point the same direction (like the "Lofi Chill" profile), the #1 result is always a clear, obvious match. No surprises there.

It also fails gracefully. Typos, unknown genres, and missing preferences don't crash it — they just quietly reduce how much the scoring can differentiate between songs.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Discovered weakness — uneven genre/mood representation creates a filter bubble.** Out of 18 songs, `lofi` has 3 entries and `chill` mood has 3 entries, while 13 of the 15 genres and 12 of the 13 moods have exactly 1 song each. This means a user whose `favorite_genre` is `lofi` gets a rich, well-differentiated top-5 list (multiple real matches to rank among), while a user who prefers `classical` or `reggae` gets at most one genuine genre match before the system falls back to filler songs that only share energy or acousticness. The system isn't intentionally biased toward pop or lofi in its scoring logic — the bias comes entirely from the dataset's uneven composition, not the Algorithm Recipe itself. In effect, users with "common" tastes in this catalog are better served than users with "rare" tastes, which is the same dynamic that produces filter bubbles in real recommenders: the model looks neutral, but the training/catalog data quietly picks favorites.

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

- **Baseline "Lofi Chill":** `genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`
- **"Happy Pop":** `genre=pop, mood=happy, energy=0.80, likes_acoustic=False`
- **Conflicting energy/mood:** `genre=rock, mood=moody, energy=0.95, likes_acoustic=False`
- **Nonexistent genre:** `genre=dubstep, mood=chill, energy=0.4, likes_acoustic=True`
- **Contradictory acousticness:** `genre=metal, mood=angry, energy=0.97, likes_acoustic=True`
- **Empty/missing preferences:** `genre="", mood="", energy=None, likes_acoustic=None`
- **Neutral energy extreme:** `genre=jazz, mood=relaxed, energy=0.5, likes_acoustic=None`
- **Genre-mood mismatch:** `genre=ambient, mood=intense, energy=0.3, likes_acoustic=False`

For each profile I looked at: did the #1 result actually make sense as "the best possible match," did the score gaps between ranks feel meaningful or arbitrary, and did any low-relevance song sneak into the top 5 just because it happened to score well on one axis.

### What surprised me

The biggest surprise was that a song can rank highly **without matching the thing a person would consider most important.** "Gym Hero" (pop, but *intense* mood, energy 0.93) shows up at #3 for the "Happy Pop" profile even though the user explicitly wants a *happy* song, not an intense one. In plain terms: Gym Hero gets credit for being pop and for being roughly the right tempo/energy, and those two points add up to a decent score even though the system completely whiffs on mood — the one thing that probably matters most to someone who typed "happy." The math is doing exactly what it was told, but the result doesn't match what a person would actually want, which is the clearest evidence that summing independent point rules can produce a "technically correct, actually wrong" recommendation.

### Pairwise comparisons

- **Baseline "Lofi Chill" vs. "Happy Pop":** The lofi/chill profile pulls in quiet, low-energy, acoustic songs (Library Rain, Midnight Coding), while the happy/pop profile pulls in loud, high-energy, produced songs (Sunrise City, Rooftop Lights). This makes sense — energy and acousticness are near-opposite ends of the scale for these two profiles, so the two top-5 lists barely overlap, showing the energy/acousticness features are actually doing real differentiating work.

- **"Happy Pop" vs. Conflicting energy/mood (rock/moody/0.95):** "Happy Pop" favors moderate-high energy (0.80) with a light, upbeat feel, while the conflicting profile pushes energy all the way to 0.95 and asks for "moody" instead of "happy." The result: completely different top songs (Storm Runner and Iron Fury show up instead of Sunrise City), which makes sense because energy is now maxed out and mood flipped to something dark — but it also shows the same flaw as the Gym Hero case: since mood and energy are still scored independently, the top result (Storm Runner) matches genre + energy while getting no credit for actually being "moody" in feel.

- **Nonexistent genre (dubstep) vs. Baseline "Lofi Chill":** Both profiles share the same mood (`chill`) and similar energy (0.35 vs 0.40), and their top-5 lists are nearly identical (Midnight Coding, Library Rain, Spacewalk Thoughts) — which makes sense, because with genre unable to match anything, the system effectively becomes a mood + energy recommender. This is a useful sanity check: it proves the system fails gracefully instead of breaking when a genre doesn't exist in the catalog.

- **Contradictory acousticness (metal + likes_acoustic=True) vs. "Happy Pop" (likes_acoustic=False):** Both profiles' #1 result is the strongest possible genre+mood+energy match for their catalog (Iron Fury for metal/angry, Sunrise City for pop/happy), and in both cases the acousticness bonus point is essentially irrelevant to who wins #1 — it only nudges lower-ranked songs around. This makes sense given the scoring weights: acousticness is worth only +1 out of a max of ~8.5, so it can't override a strong genre+mood+energy match, even when the request is internally contradictory (asking for an acoustic metal song, which doesn't exist in this catalog).

- **Empty/missing preferences vs. Neutral energy extreme (jazz/relaxed/0.5):** The empty profile produces a flat tie at score 0.00 across the board (no real ranking signal at all), while the neutral-energy profile at least has one clear #1 (Coffee Shop Stories) followed by a cluster of near-ties. This makes sense: any real target value, even a "middle of the road" one like 0.5 energy, gives the energy-closeness formula something to differentiate on, whereas `None` disables that rule entirely — showing that even a weak preference signal is better than no signal for producing a meaningful ranking.

- **Genre-mood mismatch (ambient/intense/0.3) vs. Conflicting energy/mood (rock/moody/0.95):** Both profiles ask for a mood that doesn't naturally pair with their other stated preferences (intense at low energy; moody at max energy), and in both cases the top result satisfies genre and energy but ignores mood entirely (Spacewalk Thoughts and Storm Runner respectively). This makes sense given the additive scoring design — mood is just one of four independent point sources, so a profile with self-contradictory preferences doesn't get flagged as invalid, it just quietly favors whichever two axes happen to line up.

---

## 8. Future Work  

1. **Require a minimum mood match.** Right now a song can win just by matching genre and energy, even if the mood is completely wrong (see the "Gym Hero" example in Section 7). I'd add a rule that caps the score, or filters out the song, if mood doesn't match at all.

2. **Balance the dataset.** I'd add more songs so every genre and mood has at least 2-3 examples. Right now users who like rare genres get worse recommendations just because the catalog is unfair, not because the scoring is bad.

3. **Add more preference features**, like tempo and danceability, and let users set how important each feature is to them (instead of using one fixed set of weights for everyone).

---

## 9. Personal Reflection  

Building this made me realize a recommender doesn't need to be smart to feel smart. Adding up a few simple points and sorting a list already produces results that look like "AI picked this for you," even though it's really just arithmetic.

The most interesting thing I found was that a system can be doing exactly what it was told and still give a "wrong" answer, like Gym Hero showing up for someone who wants happy songs. The bug wasn't a mistake in the code. It was a mismatch between what I told the system to care about and what a real person actually cares about.

This changed how I think about apps like Spotify. When a recommendation feels off, it's probably not broken — it's just weighing something differently than I would. And when a system quietly favors certain genres or moods, it's not always because it was designed that way on purpose. Sometimes it's just because the training data wasn't balanced, the same way my 18-song catalog wasn't.

---

## 10. Reflection on the Engineering Process

**Biggest learning moment.** The Gym Hero problem was it. I expected bugs to look like crashes or wrong numbers. Instead, the code ran perfectly and still gave a bad answer. That's when it clicked that scoring rules and ranking rules are two separate jobs, and neither one alone can catch a mistake the other one makes.

**How AI tools helped, and when I double-checked them.** The AI assistant was fastest at boilerplate: writing the CSV loader, the sort-and-slice ranking logic, and formatting terminal output. That's the kind of code where there's basically one right way to do it, so I trusted it. Where I double-checked things was the actual scoring weights and the "why" behind a result — like when I asked it to verify the energy math stayed bounded to [0, 4] after doubling the weight. I didn't just take "the math is valid" as an answer; I re-ran the profiles myself and looked at the real scores to confirm nothing went negative or broke. Anywhere the AI made a judgment call about what a song "should" score, I checked it against my own sense of whether the result made sense.

**What surprised me about simple algorithms feeling like recommendations.** Adding up four numbers and sorting a list is not complicated. But the second it prints "Because: matches favorite genre, matches favorite mood" next to a song title, it feels like something is understanding you. I didn't expect such a thin layer of logic to produce something that felt personal. It made me a lot more skeptical of "AI-powered" recommendation claims in general — sometimes "AI" is just points and sorting with good copywriting on top.

**What I'd try next.** I'd fix the Gym Hero problem for real, by requiring at least a partial mood match instead of letting genre and energy fully compensate for a missed mood. I'd also balance the dataset so every genre has a fair number of songs, and I'd try swapping the additive scoring for a similarity-based approach (comparing feature vectors with distance instead of separate point rules) to see if it produces noticeably different, and hopefully better, recommendations.
