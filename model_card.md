# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

This recommender suggests 5 songs from a 20-song catalog based on a user's
preferred genre, mood, energy, valence, and danceability. It assumes the user
has a single, consistent taste profile. This is for classroom exploration only,
not for real users.

---

## 3. How the Model Works

Each song gets a score based on how well it matches what the user wants. If the
mood matches exactly, the song gets a big bonus. If the genre matches, it gets
a smaller bonus. For numeric features like energy and valence, the score is
based on closeness — a song that is very close to your target energy scores
nearly full points, while one that is far away scores almost nothing. All the
points are added up, songs are sorted highest to lowest, and the top 5 are
returned.

---

## 4. Data

The catalog has 20 songs. The original 10 came with the starter project and
cover pop, lofi, rock, ambient, jazz, synthwave, and indie pop. I added 10 more
to include r&b, hip-hop, classical, metal, indie folk, latin, electronic,
country, soul, and chillwave. Moods in the dataset include happy, chill,
intense, relaxed, focused, moody, romantic, confident, peaceful, angry, sad,
euphoric, nostalgic, melancholy, and dreamy. The dataset still skews toward
Western genres and does not represent global music styles like afrobeats, k-pop,
or reggae.

---

## 5. Strengths

The system works best when the user has a clear, specific taste. The Chill Lofi
and Deep Intense Rock profiles both produced near-perfect #1 results (6.43 and
6.42 out of 6.5) because the catalog had strong matches. The scoring is also
fully transparent — every recommendation comes with an explanation of exactly
why it ranked where it did, which makes it easy to audit and understand.

---

## 6. Limitations and Bias

The system has a strong mood and genre lock-in problem — because mood and genre
matches award fixed bonus points (2.0 and 1.5), a song that perfectly matches
both will almost always rank #1 regardless of how far off its numeric features
are. This was revealed by the adversarial profile, where a quiet low-energy
folk song ranked #1 for a user who wanted high-energy music, simply because
the mood and genre labels matched.

The dataset is also too small and unevenly distributed to avoid filter bubbles.
Lofi has 3 songs, pop has 2, and most other genres have only 1 — so a lofi user
will always see the same 2-3 songs at the top with very little variety.

Finally, the system treats all users identically — there is no concept of
context. A user who wants chill music at midnight and high-energy music at the
gym is represented by a single static profile, which means half their actual
taste is always ignored.

---

## 7. Evaluation

I tested four user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock,
and an adversarial profile (high energy but sad mood).

The Chill Lofi and Deep Intense Rock profiles returned results that matched
intuition — the top songs were genuinely good fits. The High-Energy Pop profile
surfaced Sunrise City at #1, which makes sense, but Gym Hero only appeared at
#3 because it missed the mood match even though it is the most energetic pop
song in the catalog.

The biggest surprise was the adversarial profile. Asking for high energy (0.90)
but a sad mood returned 3AM Thoughts as #1 — a quiet indie folk song with
energy of only 0.33. The mood and genre bonus (3.5 points) completely overrode
the energy mismatch. This shows the system can be "tricked" by conflicting
preferences, and that label-based bonuses are too powerful relative to numeric
proximity scores.

I also ran a weight shift experiment — doubling energy weight and halving genre
weight — which caused rankings to shift noticeably, confirming that the weights
have a real and meaningful effect on output.

---

## 8. Future Work

- Add diversity enforcement so the top 5 always includes at least 3 different
  genres
- Support multiple mood preferences instead of one, such as "chill or focused"
- Replace fixed label bonuses with soft similarity scores so mood and genre do
  not completely dominate
- Expand the catalog significantly — 20 songs is too small to avoid repetition

---

## 9. Personal Reflection

Building this made me realize how much hidden influence the weight values have.
Small changes to a number like genre weight visibly changed which songs appeared
in the top 5, which means real platforms like Spotify are making similar choices
at massive scale — and those choices shape what music millions of people ever
discover.

The adversarial experiment was the most interesting part. I expected the system
to at least partially respect the high energy preference, but the mood bonus was
so strong it overrode everything else. That made me think about how real apps
might similarly lock users into a "vibe" they expressed once, even if their
actual needs in the moment are different.