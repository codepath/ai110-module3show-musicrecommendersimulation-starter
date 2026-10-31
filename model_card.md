# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate

The recommender generates recommendations for the top 5 songs that match the user's taste profile. They are ranked in order of highest scores using the weights applied to the four main features: genre, mood, energy, and if accoustic music is preferred.

- What assumptions does it make about the user

The system assumes the users value mood more heavily than genre. Additionally, energy is heavily weighted because it is a numeric feature. The assumption is that these weight choices reflect what most users prefer.

- Is this for real users or classroom exploration 

This is for classroom exploration but it can be adapted for real users with some enhancements.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)

As stated earlier, there are four features used. These are genre, energy, mood, and whether or not accoustic music is preferred.

- What user preferences are considered

The user preferences that are considered are directly mapped to the four features above. They are represented by these four variables:   favorite_genre, favorite_mood, target_energy, and likes_acoustic.

- How does the model turn those into a score

The mode assigns four scores based on the four features as follows:

-- Energy Score is 1 minus the difference between a given song's energy score and the target energy score from the user's preferences.
-- Both Mood Match and Genre Match are equal to 1 if there is a match between the song's attributes and the user's preferences. Otherwise, they are equal to zero if there is no match.
-- The Accoustic Score is equal to the acousticness value for a given song if the user likes acoustic songs. If they do not, then it is the difference between 1 and the song's acoustic score.

After these scores are calculated, a weighted total score is derived using this formula: 0.40 * energy_score + 0.25 * mood_match + 0.20 * genre_match + 0.15 * acoustic_score. The maximum score is equal to 1 for a perfect match.

- What changes did you make from the starter logic 

The starter logic was not implemented at all in the codebase. There were hints about using genre, mood, and energy as features with a basic rubric where you assign +2.0 points for a genre match, +1.0 point for a mood match, and similarity points based on how close the song's energy is to the user's target. The actual implementation weighs energy higher than the others, elevates mood above genre, and adds acousticness as a consideration.

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

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
