# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch 1.0

---

## 2. Intended Use  

This recommender system is designed to suggest songs based on a user’s preferences such as genre, mood, energy level, and whether they prefer acoustic music. It generates a ranked list of songs from a small dataset by comparing each song’s attributes to the user’s taste profile.

The model assumes that users have clear preferences (e.g., a favorite genre and mood) and that these preferences can be represented using simple numeric and categorical features. This system is intended for classroom exploration and learning purposes, not for real-world deployment. 

---

## 3. How the Model Works  

The model uses a content-based approach, meaning it compares each song directly to the user’s preferences instead of learning from other users.

Each song has features like genre, mood, energy, and acousticness. The user provides preferences for these same attributes, such as a favorite genre, preferred mood, and target energy level.

The model assigns a score to each song using a weighted system:

Songs get more points if the genre matches the user’s favorite genre
Songs get additional points if the mood matches
Songs get points based on how close their energy is to the user’s target energy
Songs get points based on whether they match the user’s acoustic preference

After scoring all songs, the model sorts them from highest to lowest score and returns the top recommendations. Compared to the starter logic, I refined the weighting system and added clearer explanations for why each song was recommended.

---

## 4. Data  

The model uses a small dataset of songs stored in songs.csv. The dataset includes features such as genre, mood, energy, tempo, valence, danceability, and acousticness.

The dataset contains a limited number of songs and represents only a small range of genres and moods, such as pop, lofi, and chill. I did not significantly expand the dataset, so the recommendations are limited to what is available.

The dataset also does not include many important aspects of musical taste, such as lyrics, artist similarity, language, or cultural context, which limits how realistic the recommendations can be.

---

## 5. Strengths  

This system works well for users with clear and simple preferences, such as someone who consistently prefers one genre and mood. The scoring system effectively captures patterns like matching genre and mood while also considering energy levels.

The recommendations often matched intuition, especially when a song aligned closely with all user preferences. The model is also easy to understand and explain, which is a strength compared to more complex black-box systems.

---

## 6. Limitations and Bias 

One limitation of the system is that it strongly prioritizes exact genre and mood matches. Songs that are similar but not labeled with the exact same category may be ranked lower, reducing diversity.

The model also ignores many important features such as lyrics, artist relationships, and listening history, which are important in real-world recommendation systems.

Additionally, the scoring system may unintentionally favor certain users, such as those with more common or well-represented genres in the dataset. Users with niche preferences may receive less accurate recommendations.
---

## 7. Evaluation  
I evaluated the recommender by testing multiple user profiles with different preferences.

For example, one user preferred pop, happy, and high-energy songs, while another preferred lofi, chill, low-energy, and acoustic songs. I checked whether the top-ranked songs matched these preferences.

I looked at which song ranked first and analyzed why it received the highest score. One interesting observation was that songs with very close energy levels still ranked lower if they did not match genre or mood, showing that those features had stronger influence.

---

## 8. Future Work  

In the future, I would improve the model by adding more features such as tempo ranges, valence, and lyrical themes. This would allow for more nuanced recommendations.

I would also improve diversity by ensuring the recommender does not only return songs with exact matches, but also includes similar songs from related genres.

Additionally, I would add better explanations for recommendations and possibly support more complex user profiles with multiple preferences.

---

## 9. Personal Reflection  

Through this project, I learned how recommender systems turn user preferences and item features into numerical scores that drive ranking decisions. It helped me understand how even simple systems can produce meaningful recommendations.

One surprising insight was how sensitive the system is to weighting choices. Small changes in weights can significantly change which songs are recommended.

This project also made me realize that real-world music recommendation systems are much more complex and rely on far more data, but the core idea of scoring and ranking still applies.