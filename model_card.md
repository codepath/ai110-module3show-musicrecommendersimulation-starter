# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder takes one user's stated taste profile (a favorite genre, a favorite mood, a target energy level, and whether they like acoustic or produced sound) and returns a ranked list of songs from a fixed catalog that best match that profile, with a plain-language explanation for each pick.

It assumes the user already knows roughly what they want (a genre, a mood, an energy level) rather than trying to infer taste from listening history — there is no behavioral data involved at all. This is a **classroom exploration tool**, not a production recommender: it is meant to demonstrate how a basic content-based scoring and ranking system works, not to serve real listeners.

---

## 3. How the Model Works  

Every song in the catalog gets compared to the user's profile and given points for each way it matches:

- It gets **2 points** if the song's genre is exactly the user's favorite genre.
- It gets **1 point** if the song's mood is exactly the user's favorite mood.
- It gets **up to 2 points** for energy — the closer the song's energy is to the user's target energy, the more points it earns. A song exactly at the target gets the full 2 points; a song at the opposite extreme gets 0.
- It gets **1 point** if the song's "acousticness" agrees with whether the user says they like acoustic songs or not.

All those points are added up into one score per song. Once every song in the catalog has a score, the whole list gets sorted from highest to lowest, and the top few are shown to the user, each with a short list of the reasons it scored the way it did.

The starter logic only had placeholder functions with no real scoring — I wrote the full point system above, added the "acoustic preference" rule on top of genre/mood/energy, and made sure every recommendation comes back with human-readable reasons instead of just a number.

---

## 4. Data  

- The catalog has **18 songs** (10 from the starter file, plus 8 I added).
- Each song has: title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness.
- I added songs in genres that weren't in the starter set — blues, r&b, metal, folk, edm, reggae, country, and classical — and moods like sad, romantic, aggressive, nostalgic, energetic, uplifting, and dark, so the catalog could support more varied user profiles.
- Even at 18 songs, this is a tiny catalog. It's missing huge swaths of real musical taste: no hip-hop, no world music, no live/instrumental variety within a genre, and no representation of songs that blend genres. It also has no lyrics, artist popularity, or release date — all things a real system would use.

---

## 5. Strengths  

- For a user whose genre, mood, and energy preferences all point to the same kind of song (e.g., "High-Energy Pop" or "Chill Lofi"), the top results feel right — the highest-scoring song in each case is a clear, intuitive match on all three fronts.
- The explanation strings make the reasoning fully auditable — you can see exactly which rule contributed how many points to any recommendation, which is rare even in real production recommenders.
- Because scoring is just arithmetic, the system is perfectly consistent and reproducible: the same profile always produces the same ranked list.

---

## 6. Limitations and Bias 

The scoring logic over-relies on genre and mood as blunt "yes/no" signals worth a combined 3 points, while energy is the only feature that scales smoothly with how close the match actually is. This means a song can win purely by matching genre and mood even when its energy is nowhere near the target — I confirmed this with an adversarial "Energetic but Sad" profile (genre=blues, mood=sad, energy=0.9), where the top recommendation was a slow, low-energy blues track (energy 0.30) that only barely beat out songs whose energy was actually close to 0.9 but didn't match genre/mood at all. In other words, the system can satisfy the *labels* a user picked while ignoring the *feeling* those labels were supposed to represent when they conflict. The catalog is also unbalanced — pop and lofi are the best-represented genres because they came from the starter file, so any profile favoring those genres has more good candidates to choose from than a profile favoring, say, classical or reggae, which only has one song each. That's a filter-bubble risk baked into the data, not just the math: an underrepresented-genre fan gets weaker, less varied recommendations no matter how good the scoring formula is.

---

## 7. Evaluation  

I tested four profiles end-to-end through python -m src.main: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and an adversarial edge case, **Energetic but Sad** (conflicting energy=0.9 with mood=sad). I also ran one logic experiment: halving the genre weight (2.0 → 1.0) and doubling the energy weight (max 2.0 → max 4.0) for the High-Energy Pop profile.

- **High-Energy Pop vs. Deep Intense Rock:** the pop profile surfaces upbeat, danceable songs (Sunrise City, Gym Hero), while the rock profile surfaces the same "high energy" region of the catalog but filtered toward the rock/intense label (Storm Runner tops the list at score 5.98). This makes sense — both profiles target similarly high energy, but the genre/mood bonus is what actually separates a rock recommendation from a pop one, since several songs in the catalog sit in a similar energy range regardless of genre.
- **High-Energy Pop vs. Chill Lofi:** these two profiles produce almost entirely non-overlapping top-5 lists (only high vs. low energy songs show up in each, respectively), which makes sense since they target opposite ends of the energy scale as well as different genres and moods — this is the case where the recommender's differentiation is clearest and most intuitive.
- **Weight-shift experiment:** doubling the energy weight and halving the genre weight caused *Rooftop Lights* (an indie-pop song with no genre match but energy very close to the target) to jump ahead of *Gym Hero* (an exact genre match but a worse energy fit). This surprised me a little — it shows the ranking is genuinely sensitive to the weights chosen, not just to whether a feature matches at all. It also raises the underlying question of whether "genre" or "energy" *should* be the stronger taste signal, which isn't something the math alone can answer.
- The biggest surprise overall was the "Gym Hero" pattern: it's a pop/intense song with very high energy (0.93) and low acousticness, so it scores well for *any* profile that wants high energy and/or pop, even profiles that aren't really "about" gym music. In plain terms: "Gym Hero" is a strong all-around match on paper (loud, fast, produced, upbeat-labeled), so it keeps showing up as a runner-up across very different profiles — a stand-in for how a single well-rounded, high-energy song can dominate recommendations for many different listeners, the same way a handful of "generically catchy" songs can dominate real streaming charts.

---

## 8. Future Work  

- Add more songs per genre (especially the underrepresented ones I added — blues, classical, reggae, country) so the catalog can no longer bias results just from data imbalance.
- Let feature weights be tunable per user rather than fixed constants, so the relative importance of genre vs. mood vs. energy could reflect how strongly *that specific* user cares about each one.
- Add a diversity/de-duplication step to the ranking so that the top 5 don't all come from the same artist or an extremely narrow energy band, the way "Sunrise City" and "Night Drive Loop" (same artist) both showed up together in one profile's results.

---

## 9. Personal Reflection  

The biggest learning moment was seeing how a system built from three or four simple if statements and one linear-similarity formula could still produce results that *feel* like genuine taste-matching — right up until an adversarial profile exposed exactly where the illusion breaks down. Using an AI coding assistant helped me move quickly from "recipe" to working code and helped me think through edge cases (like the conflicting energy/mood profile) that I might not have designed myself, but I still had to double-check its suggested formulas by hand-tracing a couple of songs through the scoring math to make sure the numbers actually meant what I thought they meant. What surprised me most is how much *perceived* intelligence in a recommender comes from the explanation text, not the math — printing "Because: genre match, mood match" next to a score makes an extremely simple weighted sum feel like a thoughtful recommendation. If I extended this project, I'd want to try blending in a lightweight collaborative-filtering signal (even something as simple as "users who set this profile also liked...") so the system isn't purely dependent on a handful of hand-picked features.
