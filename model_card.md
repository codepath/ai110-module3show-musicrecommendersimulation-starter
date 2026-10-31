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

Think of the recommender as a judge who gives every song in the catalog a score out of 4 points, then hands you the five highest scorers.

**What the judge knows about you.** You tell it three things: your favorite genre, your favorite mood, and how energetic you want your music to be (a number from 0, very calm, to 1, very intense).

**What the judge looks at in each song.** Only three things: the song's genre, its mood, and its energy level. The catalog also records tempo, valence, danceability, and acousticness, but the score does not use them.

**How the points are given.**

- **Genre: 2 points.** If the song's genre is the same as your favorite, it gets 2 points. If not, it gets none.
- **Mood: 1 point.** If the song's mood is the same as your favorite, it gets 1 point. If not, it gets none.
- **Energy: up to 1 point.** The closer a song's energy is to the level you asked for, the more points it gets. A song that hits your target exactly gets the full point, and the score drops as the gap grows. The model does not assume more energy is better. If you ask for calm music, a loud song is penalized just like a too-quiet song would be for someone who wants intensity.

Genre is worth twice as much as mood on purpose. I treated genre as the more stable sign of someone's taste, and mood as a helpful but weaker hint. Energy is worth the least, so it works mainly as a tiebreaker between songs that match the same categories.

**How the list is made.** The judge scores every song one at a time, sorts them from highest to lowest, and shows the top five. Next to each song it prints the reasons behind the score, such as "genre match (+2.0)", so you can see exactly why a song was picked.

**A worked example.** For someone who wants pop, happy, and energy 0.8, "Sunrise City" (pop, happy, energy 0.82) scores 3.98 out of 4: 2 for genre, 1 for mood, and 0.98 for being very close on energy. "Gym Hero" (pop, intense, energy 0.93) scores 2.87: it earns the genre points but not the mood point.

**What changed from the starter logic.** The starter project only had empty placeholders for loading songs, scoring them, and ranking them. I filled these in with the recipe above and added the printed reasons and a cleaner terminal layout. I picked the point values (2, 1, and 1) myself, so they are a design choice and not a proven best answer.

**Known blind spots of this approach.** Because genre and mood are all-or-nothing, a song that is "almost" the right genre, like indie pop for a pop fan, gets no credit. And because genre counts twice as much as mood, a song in your genre can outrank one that matches your mood. This is covered in more detail in the Limitations and Bias section.

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
