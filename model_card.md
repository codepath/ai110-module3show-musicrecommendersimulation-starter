# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Name: Musical Heaven 1.0
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Answer: This recommender is designed for simple music discovery and producing enjoyment
of vibing to your favorite music. For instance, the user finds songs that match their preferred genre, mood, energy level, and occasionally acoustic sounds. However, the intention behind my system is to show a basic music recommender system works rather than to replace a real-world music streaming service.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Answer: The recommender works by giving each song a score based on how well it matches a user's taste profile. The strongest signals are genre and mood because those are the clearest indicators of a musical vibe. It also considers how close the song's energy level is to the user's preferred energy, and it gives a smaller bonus if the user likes acoustic music. For instance, the system tries to find songs that feel like the right fit for the user's mood and style, rather than just picking the most popular or random options. Compared with the starter logic, this version gives more importance to energy and uses acousticness as a smaller tie-breaker.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

Answer: The recommender uses a small catalog of 18 songs with a variety of genres, moods, and musical styles. The dataset includes different kinds of genres, such as pop, lofi, rock, indie pop, synthwave, and more. No data was added or removed. Because of the small dataset, there are parts of musical taste missing, which means the simple music recommender system can't represent every kind of musical taste.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Answer: The system works well for users who have clear and consistent preferences of their music choices. For instance, my system does a good job when a user wants upbeat pop, intense rock, or calm lofi due to those preferences being easy to match with the available data. Additionally, my system does a great job showing how a user's preferences being changed alters the song rankings. In many cases, the recommendations feel intuitive whenever the user's requested genre, mood, and energy level all line up.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Answer: The recommender system uses exact string matching for genre and mood, which means a song receives zero credit if it doesn't perfectly match the user's stated preferences. For example, a user who enjoys "rock" music receives no genre score for a "metal" song, even though these genres are musically similar. This rigidity causes the system to struggle when the dataset lacks songs with exact genre-mood combinations that users want—such as the "No Match Fallback" test case with country-melancholic music. As a result, recommendations become overly narrow and can fail to surface musically relevant songs that differ only slightly in classification.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

### Profiles Tested

I tested six distinct user profiles to cover different musical tastes and edge cases:

1. **High-Energy Pop**: A user who loves upbeat, happy pop music (think workout playlists)
2. **Chill Lofi**: A user who wants mellow, acoustic background music for studying
3. **Deep Intense Rock**: A user who loves loud, energetic rock with an intense vibe
4. **Conflicting Mood-Energy**: A user who wants pop music that's sad but very energetic (a mismatch to see how the system handles conflicting preferences)
5. **No Match Fallback**: A user seeking country-melancholic music with low energy (testing what happens when the exact combination barely exists)
6. **Acoustic Bonus Trap**: A user who likes intense rock but prefers it acoustic and quiet (another contradiction to stress-test the weighting)

### Key Findings and Comparisons

**High-Energy Pop vs. Chill Lofi**

These two profiles show the most dramatic difference. When you run High-Energy Pop, songs with high energy (around 0.8) and pop genre dominate—imagine upbeat tracks perfect for the gym. When you run Chill Lofi, the same songs score near zero because they fail both the genre and mood tests. Instead, lofi tracks with low energy (around 0.4) and acoustic instruments rise to the top. This proves the genre and mood filters are working correctly: a pop song simply has no place in a lofi playlist, even if it's technically well-produced.

**Deep Intense Rock vs. Acoustic Bonus Trap**

Here's where I discovered something surprising. Both profiles prefer rock music, but their energy requirements pull in completely different songs. Deep Intense Rock pulls high-energy rock tracks (energy ~0.9), while Acoustic Bonus Trap (which prioritizes acoustic bonus) struggles because it's asking for intense rock that's also very quiet and acoustic. In real datasets, truly acoustic rock is rare, so Acoustic Bonus Trap either gets a weak score for regular rock songs or occasionally finds the one folk-rock track that happens to be acoustic. This shows that contradictory preferences create mediocre recommendations—the system can't satisfy both constraints equally well.

**Conflicting Mood-Energy vs. High-Energy Pop**

Both want high energy (0.8-0.9), but Conflicting Mood-Energy asks for *sad* pop while High-Energy Pop asks for *happy* pop. If a pop song is very energetic, it's usually tagged as happy. So Conflicting Mood-Energy gets lower scores overall because it loses the mood-match bonus on high-energy songs. The recommendations become a compromise: maybe a slower sad ballad that doesn't match energy, or a high-energy song that doesn't match the sad mood. This is where I realized the system rewards consistency—when your preferences align (happy + energetic), you get better matches.

**No Match Fallback**

This profile taught me about dataset limitations. The user wants low-energy country with a melancholic mood—a valid combination, but if the song catalog has only three country songs and none are truly melancholic, every country song scores the same (low) points on mood. The recommendations become almost random among weak matches. This exposed a weakness: when the exact genre-mood pair doesn't exist, the system has no graceful fallback and just returns mediocre options.

### What Surprised Me

I expected Acoustic Bonus Trap to always pick the most acoustic songs, but instead I discovered that when acoustic preference conflicts with genre/mood priorities, the system can't balance it well. An intense rock song with low acousticness score (say, 0.1) multiplied by the acoustic bonus (0.5 max) only adds 0.05 points—barely helping. This showed me that the acoustic preference is treated as a "nice-to-have" bonus rather than a dealbreaker, which might not match real user expectations.

I also ran a simple manual test: if I change Conflicting Mood-Energy to have sad+low energy (a more realistic combination), the recommendations improve dramatically. This proved the system works best when user preferences are internally consistent.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Answer: In the future, I would improve this recommender by expanding the dataset more to cover a wider range of genres, moods, and artists. I would also add more features, such as tempo, danceability, and valence, to make the recommendations more realistic and detailed. Another improvement is to handle conflicting preferences more gracefully, so the system can better balance trade-offs instead of producing overly narrow results. Finally, I make the recommendations easier to explain so that users can understand why each song was suggested.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Answer: My biggest learning moment during the project is how music recommenders work where I had to build one from scratch by implementing my methods and objects to ensuring users are listening to music that produces their musical vibe, and those methods include a scoring system and the weights of each category. AI tools, like Claude Code and its chat assitant, was very essential to the project by providing a clear and efficient cycle on how users are getting the right song recommendations, including how the math works for the weights carried in each category and what fixes are needed to bring my simple music recommender system to life. Additionally, I would double-check the information provided by my AI tools whenever it goes against my idea of how my music recommender works, such as the math not aligning with the finalized algorithm recipe essential to the music recommender's development. Then, I'm amazed with how simple algorithms can still "feel" like recommendations because they don't need to be complex to showcase their usefulness by following these adjustments, which are having structured input and clear user preferences. Finally, if I extended this project, I would try to make the simple music recommender more realistic by having a larger dataset and adding more features. Furthermore, the new features would include tempo, valence, or danceability to capture more of a song's feeling.