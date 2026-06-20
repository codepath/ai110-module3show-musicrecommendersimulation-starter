# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatcher 1.0**

---

## 2. Intended Use

This recommender suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration — not for real users or production use. It assumes the user can describe their taste with a few simple preferences.

---

## 3. How the Model Works

The system compares a user's preferences to each song in the catalog and gives it a score. Genre and mood either match or they don't — a match adds points, no match adds nothing. Energy is scored by closeness — the nearer a song's energy is to what the user wants, the more points it gets. The final score is a weighted sum: genre counts the most (0.40), then mood (0.35), then energy (0.25). Songs are ranked by score and the top results are returned with a short explanation.

---

## 4. Data

The catalog has 18 songs. Genres include pop, lofi, rock, jazz, synthwave, ambient, indie pop, r&b, hip hop, classical, country, metal, and folk. Moods include happy, chill, intense, relaxed, focused, moody, romantic, and sad. I expanded the original 10-song dataset to add more variety. Some genres still only have one song, so certain user profiles get fewer good options than others.

---

## 5. Strengths

The system works well when the user's preferences match what's in the catalog. Profiles like lofi/chill, pop/happy, and rock/intense all got strong, intuitive results. The scoring logic is transparent — every recommendation comes with a plain-language explanation of why it matched. It's easy to understand and easy to adjust.

---

## 6. Limitations and Bias 

The biggest limitation I found is that the system scores each feature independently — it has no way to tell whether a combination of preferences actually makes sense together. For example, when I tested a "sad folk, high energy" profile, the top pick was correct, but the next results were intense rock and pop songs that matched on energy alone. A real listener in a sad mood would never want those, but the system had no way to filter them out.

Genre is also a hard ceiling. If a user's preferred genre doesn't exist in the catalog — like reggae — the maximum possible score drops to 0.60 regardless of how well everything else matches. This means some users are structurally disadvantaged just because of what's in the dataset, not because of anything they did wrong.

Mood matching is binary — a song either matches or it doesn't. There's no sense of "closeness" between moods, so "chill" and "relaxed" are treated as completly different even though most people would consider them similar. This creates some unintuitive gaps in the rankings.

Finally, the catalog is small and unevenly distributed. Some genres have two or three songs, others only one. Users whose taste aligns with well-represented genres (like lofi or pop) get much better results than users whose taste falls outside what's covered. The system doesn't account for this imbalance at all.

---

## 7. Evaluation  

I tested six user profiles — three core and three edge cases — by running the recommender and checking whether the top results matched what a real listener with those preferences would actually want.

**Core profiles (Jackie, Alex, Sam)** all performed well. Jackie's lofi/chill profile surfaced *Midnight Coding* and *Library Rain* as the top two, which felt right. Alex's pop/happy profile gave *Sunrise City* a perfect 1.00 score, which made sense since it matched on all three features. Sam's rock/intense profile correctly ranked *Storm Runner* first.

**Edge cases revealed the real weaknesses.** Jordan's conflicting profile (sad folk, high energy 0.9) got the right top pick, but songs #2 and #3 were intense rock tracks that had nothing to do with a sad mood — they just happened to match on energy. That was the most surprising result because it showed the system doesn't understand that some combinations of preferences conflict with each other.

Riley's reggae profile was another eye-opener. With no reggae in the catalog, every song started at zero for genre, and the highest score anyone could reach was around 0.56. The system still returned results, but they didn't feel meaningful — it was basically guessing based on mood and energy alone.

I also ran a weight shift experiment — doubling energy to 0.50 and halving genre to 0.20 — to see if the balance of features changed the results. It improved some cases (Riley got slightly better picks) but made Jordan worse. That experiment confirmed that the original weights (genre 0.40, mood 0.35, energy 0.25) were the better choice.

---

## 8. Intended Use and Non-Intended Use

**Intended use:** Classroom exploration of how content-based recommenders work. Good for testing scoring logic with small datasets and simple user profiles.

**Not intended for:** Real music platforms, production use, or users who expect personalized results based on listening history. It does not learn over time and does not use any real user data.

---

## 9. Ideas for Improvement

- Treat mood as a hard filter so songs with a completely different mood are excluded before ranking — this would fix the Jordan edge case
- Add genre groupings as a fallback (eg. reggae → world music) so users whose genre isn't in the catalog still get reasonable results
- Expand the catalog significantly and balance genres so every user type has enough options to choose from

---

## 10. Personal Reflection

The biggest surprise was the edge cases. I expected the system to struggle with missing genres, but I didn't expect it to return intense rock songs for someone who wanted sad folk music. Technically the math was right — those songs matched on energy — but for a real listener it would have felt completely off. That gap between "mathematically correct" and "actually useful" was the most interesting thing I discovered.

The other moment that stuck with me was Riley's reggae profile. The system still returned results with seemingly confident scores, even though it had no reggae songs at all. It didn't say "I don't know" — it just gave seemingly poir choices. That made me think differently about how real recommendation systems might fail without users ever realizing it. If the data doesn't include your taste, the system doesn't tell you — it just recommends the closest thing it has.
