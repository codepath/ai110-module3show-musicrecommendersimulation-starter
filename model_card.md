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

Think of the recommender as a judge at a talent show who gives every song in the catalog a scorecard. The judge knows what the listener asked for, checks each song against that request, and adds up points. Once every song has a score, the judge lines them up from highest to lowest and hands the listener the top five.

**What the judge knows about each song.** Every song has a genre (like pop or lofi), a mood (like happy or chill), and four "sound" ratings from 0 to 1: how energetic it is, how positive it sounds (valence), how danceable it is, and how acoustic it is (guitars and pianos rather than electronic production).

**What the judge knows about the listener.** The listener gives a favorite genre, a favorite mood, how energetic, positive and danceable they want their music to be, and whether they like an acoustic sound.

**How points are given (up to 7 in total):**

- **Genre match: 2 points.** If the song's genre is exactly the listener's favorite, it gets the biggest reward. A close relative, such as "indie pop" for a pop fan, earns 1 point.
- **Mood match: 1 point.** If the song's mood is exactly the one the listener asked for.
- **Energy, positivity and danceability: up to 1 point each.** These reward songs that are *close* to what the listener wants, not songs with the highest values. If you ask for medium energy, a medium-energy song earns nearly a full point, while a very intense song earns less, even though it has "more" energy.
- **Acoustic sound: up to 1 point.** Acoustic songs score well for listeners who like an acoustic sound, and electronic or produced songs score well for everyone else.

**Why genre is worth more than mood.** The sound ratings already hint at mood: happy songs tend to be energetic and positive, and chill songs tend to be calm. Mood is partly counted twice, so it gets a smaller bonus. Nothing else tells the judge a song's genre, so genre gets the larger bonus.

**Why the labels don't decide everything.** Genre and mood together are worth at most 3 points, while how a song sounds is worth up to 4. A song with the right label that sounds completely wrong can still be beaten by a song that sounds right.

**Explaining the choice.** Every time the judge gives points, it writes down why, for example "genre match: pop (+2.0)" or "energy 0.82 vs target 0.70 (+0.88)". Each recommendation comes with this list, so the listener can see why the song was picked.

**Changes from the starter logic.** The starter version had no scoring: it simply returned the first five songs in the file. I added the point system above, partial credit for related genres, the "closeness" scoring for the sound ratings, and a written reason for every point given. Tempo and artist are not used. Tempo mostly repeats what energy already measures, and in a 20-song catalog, rewarding the same artist would just repeat the same two names.

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
