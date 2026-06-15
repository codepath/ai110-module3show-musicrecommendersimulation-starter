# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

This recommender suggests songs from a small catalog based on a user's genre, mood, energy, and acoustic preference. It tries to rank songs by how closely they match the user's taste profile.

---

## 3. Data Used

The dataset has 10 songs. Each song includes genre, mood, energy, tempo, valence, danceability, and acousticness. The data is small and not very diverse. Some moods and genres are missing, so certain users cannot get strong matches.

---

## 4. Algorithm Summary

Each song gets a score from four signals. Genre match adds 1.5 points. Mood match adds 1.5 points. Energy adds up to 2.0 points based on how close the song energy is to the target energy. Acoustic preference adds 1.0 point when it aligns. Songs are sorted by total score and the top results are returned.

---

## 5. Observed Behavior / Biases

The model works best when the user likes genres and moods that are already in the dataset. It struggles when the user asks for missing genres like classical or missing moods like sad. A strong pattern is the genre filter bubble: if only one song fits a genre, that song keeps appearing at the top. Another limitation is the hard acoustic cutoff, which treats near values too differently.

---

## 6. Evaluation Process

I tested three standard profiles and five edge-case profiles. I checked whether top results made sense for each profile and whether explanations matched the scores. I also ran two experiments: changing weights and removing mood. The most surprising result was that a sad high-energy profile still got upbeat pop songs near the top. I also ran tests to confirm ranking order and non-empty explanations.

---

## 7. Intended Use and Non-Intended Use

Intended use: classroom learning, simple demos, and understanding recommendation logic.

Non-intended use: real product decisions, high-stakes personalization, or representing a user's full music identity. The dataset is too small and too narrow for those uses.

---

## 8. Ideas for Improvement

1. Expand the dataset with more genres, moods, and artists.
2. Replace the acoustic binary rule with a smooth similarity score.
3. Add diversity constraints so top results are less repetitive.

---

## 9. Personal Reflection

My biggest learning moment was seeing the High-Energy Sad profile still get upbeat pop songs at the top. That made it clear that the scoring math can be "correct" but still feel emotionally wrong for a real user. AI tools helped me move faster by generating profile ideas, test cases, and quick explanations, but I had to double-check outputs in the terminal because some suggestions looked reasonable on paper but did not match the actual ranking behavior. I was surprised that such a simple weighted formula could still feel like a real recommender when the top songs matched the profile well, especially for Chill Lofi and Deep Intense Rock. If I extend this project, I would add more songs first, then add a diversity rule and smoother acoustic scoring so results feel less repetitive and more human.
