# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
 
- **VibeMatch 1.1**  

---

## 2. Intended Use  
 
This music recommender is designed to suggest songs from a small, local catalog of 20 tracks. It is built for **classroom exploration** to understand how basic content-based filtering algorithms operate. It assumes the user has a clear preference for a specific genre, mood, and energy level, and it uses those to generate a ranked list of the top 5 matches.

---

## 3. How the Model Works  
 
- In our initial version, we used a **Genre-Dominant** approach (Genre = +2.0, Energy = +1.0) to ensure high name-brand consistency.
- In our **VibeMatch 1.1** experiment, we shifted to an **Energy-Dominant** approach (Genre = +1.0, Energy = +2.0) to better capture the "sound" of the music.

Think of our model as a specialized grader. For every song in the catalog, it checks how well it matches your "ideal" song:
- **Energy (2.0 points)**: Re-tuned in version 1.1 to be the primary driver. It ensures the "power" of the song matches your request.
- **Genre (1.0 points)**: Still a important label, but now treated as a secondary preference after the "vibe."
- **Mood (1.0 points)**: We match tags like "happy" or "chill."
- **Acoustic (0.5 points)**: Bonus points for matching instrument preferences.

---

## 4. Data  
 
We use a local `songs.csv` file containing **20 hand-crafted song entries**. We added 10 more to the original 10 that already existed.  These represent a range of genres (pop, lofi, rock, classical, metal, etc.) and moods. A major missing piece is "lyrics" or "language"—the model only looks at technical tags and numbers, not the actual story the song tells.

---

## 5. Strengths  
 
VibeMatch 1.1 excels for **"Vibe-First" Users**. 
- **High Energy Match**: It captures patterns of intensity correctly, ensuring that if you ask for high energy, you get it—even if it's in a genre you haven't explored yet.
- **Cross-Genre Discovery**: Unlike the 1.0 baseline, this version correctly identified that a Techno song (`CYBER PUNK`) might be a better match for a "High-Energy Classical" request than a slow classical remix. It matches human intuition about the *feeling* of a moment rather than just the *category*.
- **Transparency**: The scoring rules are simple and easily tunable, allowing for clear explanations of every recommendation.

---

## 6. Limitations and Bias 
 
A major limitation of the 1.1 version is **Genre Hallucination**. Because Energy now outweighs Genre (+2.0 vs +1.0), the system can accidentally ignore a user's strict genre boundaries. This could be frustrating for a "Genre Purist" who absolutely does not want to hear Metal, even if it perfectly matches their "high energy" request.

---

## 7. Evaluation  
 
I tested the system using six profiles and ran a **Comparative Weight Experiment**. 
- **VibeMatch 1.0 Analysis**: Showed that +2.0 Genre weight made the system too rigid, recommending slow music for high-energy classical requests.
- **VibeMatch 1.1 Shift**: By doubling the Energy weight, I observed the system become much more dynamic. It correctly promoted "energetic" songs to the top, which better matched my intuition for those specific test cases.
- **Surprise**: I was surprised that such a small mathematical shift (switching 2.0 and 1.0) could fundamentally change whether a user feels "listened to" or just "categorized."

No need for numeric metrics unless you created some.

---

## 8. Future Work  
 
Next steps would be to add a **Diversity Filter**. Instead of always picking the highest score, the system could try to ensure at least one song from a *different* genre is included if its mood and energy are a perfect match. I would also investigate using **Tempo** as a feature to prevent the mismatched energy issues we saw in classical music.

---

## 9. Personal Reflection  
 
Building this made me realize that even a "simple" rule like "Genre gets +2 points" can totally change a user's experience. It made me much more aware of the "Filter Bubble"—I now see how easy it is for an algorithm to keep you in one lane just because it's the safest match for a label, missing out on the actual vibe you might be searching for.
