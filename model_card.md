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

The recommender works like a judge giving every song in the catalog a mark out of 1, then handing back the five highest marks.

**What it looks at.** You tell it your favorite genre and mood, plus how energetic, upbeat (valence) and acoustic you want your music to be. For each song it compares those wishes against the song's own details.

**How a song earns points.**

- For the three "dial" qualities, it asks how close the song is to what you want, not how high it is. A song at 0.82 energy is nearly as good as 0.80 for someone who asked for 0.80, and a 0.15 song is not. Energy counts most (35%), then acousticness (25%), then valence (20%).
- Mood and genre are simple yes-or-no checks. A matching mood adds 12% and a matching genre adds 8%. They are worth less because most genres appear only once in a small catalog.

**What you get back.** The points are added up, the songs are sorted from best to worst, and the top five are shown with a short list of reasons, for example "mood match (+0.12)". So you can always see why a song ranked where it did.

**What I changed from the starter.** The starter only loaded and returned the first few songs. I added the CSV loading, the scoring rule above and the ranking step.

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

**Weakness found: listeners with extreme tastes are served worse than listeners with middle-of-the-road tastes.** Because every feature is scored by closeness to the target, and most of the 18 songs sit in the middle of the energy, valence and acousticness ranges, a "mid" listener has many near matches while an "extreme" one has very few. In my "Extreme Targets" test (metal, peaceful, energy 0.0), the best score was only 0.52, and the only metal song was missing from the top 5. In contrast, the "Unknown Genre and Mood" profile with every target at 0.5 scored 0.72 at the top without matching a single label. Because the system always returns five results and never says "nothing fits", the extreme listener gets a confident-looking list that is really a poor match. This is a small filter bubble: the catalog and the scoring both favor average tastes, and mostly single-song genres (13 of 15 genres appear once) mean a genre-first listener rarely finds more than one match.

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
