# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

This recommender is designed to suggest songs that best match a user's musical preferences, such as genre, mood, and audio features like energy and danceability. It is intended for classroom exploration and learning about recommender systems, not for real-world deployment. The system assumes users can describe their preferences numerically and by category. It generates top-k song recommendations for each user profile, helping students understand how different features and weights affect results.

---

## 3. How the Model Works  

The model uses a scoring system that compares each song's features to a user's stated preferences. It considers genre, mood, energy, tempo, valence, danceability, and acousticness. Each feature contributes to a total score: genre and mood matches add fixed points, while numerical features add points based on how close the song is to the user's target. Recently, the energy feature was given double weight, and genre weight was halved, to test the system's sensitivity. The top-scoring songs are recommended to the user.

---

## 4. Data  

The dataset contains 20 songs, each with attributes for genre, mood, and several audio features. Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, world, chip tune, blues, folk, trap, disco, classical, latin, drum and bass, and metal. Moods range from happy and chill to intense, relaxed, and reflective. No data was added or removed from the starter set. Some genres and moods are underrepresented, and the catalog does not cover all possible musical tastes or subgenres.

---

## 5. Strengths  

The system works well for users with clear, mainstream preferences, such as those who like high-energy pop or chill lofi. It captures patterns like matching genre and mood, and rewards songs that closely fit a user's desired energy or danceability. In many cases, the top recommendations align with musical intuition, especially when the user's preferences are well-represented in the dataset. The scoring system is transparent and easy to adjust for experimentation.

---

## 6. Limitations and Bias 

One weakness observed during testing is that the system can over-prioritize songs with high energy, especially after increasing the weight for energy similarity. This sometimes causes songs with only a loose genre or mood match to appear at the top of the recommendations, reducing diversity. Additionally, the relatively small dataset means that some genres or moods are underrepresented, which can bias the results toward more common categories. The recommender's sensitivity to weight changes also highlights how a single feature can dominate the rankings if not balanced carefully. As a result, users with niche or conflicting preferences may not receive recommendations that feel accurate or personalized.

---

## 7. Evaluation  

I tested the recommender using both typical and adversarial user profiles. For each profile, I checked whether the top 5 recommendations made sense given the user's stated preferences. I looked for cases where the system was "tricked" by conflicting or extreme preferences, and compared the results to my own musical intuition. I also experimented with changing feature weights to see how the rankings shifted. This process revealed both strengths and weaknesses in the scoring logic.

---

## 8. Future Work  

Future improvements could include adding more features, such as lyrics or user listening history, to better capture complex tastes. Improving the diversity of recommendations—so the top results aren't always from the same genre or artist—would make the system more useful. More advanced explanation logic could help users understand why a song was recommended. Expanding the dataset to include more songs and genres would also reduce bias and improve accuracy.

---

## 9. Personal Reflection  

Working on this project taught me how sensitive recommender systems are to feature selection and weighting. I was surprised by how much a single weight change could affect the top results, and how easily the system could be biased by the dataset. This experience gave me a deeper appreciation for the challenges of building fair and useful music recommendation apps, and the importance of testing with a variety of user profiles.
