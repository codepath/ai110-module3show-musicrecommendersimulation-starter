# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

Final model name: **Luna Vibes 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration

Luna Vibes generates personalized music recommendations based on genre, mood, energy, and acoustic quality. For **classroom learning only**. Assumes users know what they want and have stable preferences.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Luna Vibes scores songs by assigning points: +1 for genre match, +1 for mood match. Energy and mood intensity (valence) earn fractional points based on similarity. Acousticness has user-specific weight. The system penalizes contradictory preferences (high energy + low valence = angry rock) with a 20% score reduction.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

**50 songs** across 8 genres: lofi, jazz, pop, rock, indie, electronic, folk, hip-hop. Genre representation is imbalanced—lofi/jazz have 6-7 songs each, while K-pop/reggae/country have 1-2. Missing: classical, country, K-pop, Latin music.  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition

Works well for users with **mainstream + balanced preferences** (lofi + chill + acoustic, or pop + happy + energetic). Genre and mood matching are strong signals. Covers ~50-60% of typical user profiles.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Genre bias:** Underrepresented genres lose the +1.0 match bonus, creating a filter bubble. **Conflict penalty:** Penalizes valid preferences (intense metal, angry rock). **Missing features:** Danceability and tempo ignored, filtering out users who want danceable/fast music.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

Tested 6 adversarial profiles. 
Key findings: (1) **Conflicting Preferences** (wanting sad + energetic music) were penalized despite being legitimate (angry rock). (2) **Impossible Genres** revealed hidden filtering when preferred genres are underrepresented. 
Surprise: The conflict penalty backfired—it punishes real music fans instead of catching errors.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes

### Recommendations

- **Add danceability & tempo as scoring factors** (currently ignored)
- **Refine conflict penalty**—high energy + low valence is legitimate (metal, punk)
- **Balance dataset**—add 4-5 songs per underrepresented genre  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

**Lesson:** Recommendation systems are never neutral—every design choice encodes bias. Small decisions (weighting genre heavily) invisibly favor common users and exclude edge cases. **Surprise:** The conflict penalty backfired and punished real music fans (metal, rock) instead of improving recommendations. **Changed my perspective:** I now question whether apps "don't get me" because of my tastes or their design. Algorithms are coded assumptions, not objective truth.  
