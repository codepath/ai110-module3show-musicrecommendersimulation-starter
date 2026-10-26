# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**  

It finds songs that match your vibe.  

---

## 2. Intended Use  

**Goal.** The model suggests songs from a small catalog. It gives the top five songs for one listener. Each song comes with reasons.  

**Who it is for.** It is a classroom project. It is for learning how recommenders work. It is not for real users.  

**What it assumes about the listener.**  

- The listener can say their favorite genre and mood.  
- The listener can give target numbers for energy, happiness (valence) and acoustic sound.  
- The listener wants songs close to those numbers.  

**Intended use.**  

- Learning and experiments.  
- Showing how scores turn into rankings.  
- Testing how weights change results.  

**Not intended for.**  

- A real music app. The catalog has only 18 songs.  
- Judging music quality or an artist's worth.  
- Guessing what people like from their identity.  
- Anything where a bad match would cause harm.  

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

**Size.** The catalog has 18 songs. It lives in `data/songs.csv`.  

**Columns.** Each song has an id, title, artist, genre, mood, energy, tempo, valence, danceability and acousticness. The numbers run from 0 to 1, except tempo.  

**Advanced columns.** I added five: popularity (0–100), release decade, detailed mood tags (like "cozy" or "gritty"), instrumentalness (0–1) and explicit (yes or no). I made up these values. They are a guess, not real data.  

**Genres.** There are 15 genres. Lofi has 3 songs. Pop has 2. The other 13 genres have one song each.  

**Moods.** There are 14 moods. Chill has 3 songs. Happy and intense have 2 each. The other 11 moods have one song each.  

**Changes.** I did not add or remove any songs. I only added the five columns above.  

**What is missing.**  

- Lyrics and language.  
- Real popularity and release data. The added values are made up.  
- What other people listen to.  
- Many genres, such as Latin, K-pop and gospel.  

Tempo and danceability are in the data. The model does not use them.  

---

## 5. Strengths  

**Works well for typical listeners.** The Chill Lofi, High-Energy Pop and Deep Intense Rock profiles all gave sensible lists.  

**Closeness works.** Scoring by "how close" beats scoring by "how high". A calm listener does not get loud songs.  

**It matched my gut.**  

- Sunrise City won for pop and happy.  
- Both lofi chill songs led for the lofi listener.  
- Storm Runner won easily for rock.  

**It explains itself.** Every song comes with reasons, like "mood match (+0.12)". You can see why it ranked where it did.  

**Opposite tastes get opposite lists.** The pop and lofi profiles shared no songs.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

**Weakness found: listeners with extreme tastes are served worse than listeners with middle-of-the-road tastes.** Because every feature is scored by closeness to the target, and most of the 18 songs sit in the middle of the energy, valence and acousticness ranges, a "mid" listener has many near matches while an "extreme" one has very few. In my "Extreme Targets" test (metal, peaceful, energy 0.0), the best score was only 0.52, and the only metal song was missing from the top 5. In contrast, the "Unknown Genre and Mood" profile with every target at 0.5 scored 0.72 at the top without matching a single label. Because the system always returns five results and never says "nothing fits", the extreme listener gets a confident-looking list that is really a poor match. This is a small filter bubble: the catalog and the scoring both favor average tastes, and mostly single-song genres (13 of 15 genres appear once) mean a genre-first listener rarely finds more than one match.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

**Profiles tested (six).** Three typical listeners: **A. High-Energy Pop**, **B. Chill Lofi** and **C. Deep Intense Rock**. Three tricky ones built to confuse the system: **D. Sad but Energetic** (wants classical and melancholy, but loud), **E. Unknown Genre and Mood** (asks for a genre and mood that don't exist in the catalog, with every number set to the middle) and **F. Extreme Targets** (metal but peaceful, zero energy, maximum happiness). For each one I checked whether the top five matched what I'd expect a real listener to want. I also tried a version where energy counted double and genre counted half, to see how fragile the rankings were.

**What surprised me**

- **Why *Gym Hero* keeps showing up for "Happy Pop" fans.** *Gym Hero* is a pop song, so it gets the genre bonus. It is also loud and upbeat with almost no acoustic sound, which is just what a happy pop listener's numbers ask for. The only thing it gets wrong is its mood label ("intense", not "happy"), and that costs only 0.12 points, which is less than it gains from sounding right. So the system treats it as a pop song that sounds the part, and it doesn't know that a workout track feels different from a feel-good one.
- **The system never says "nothing fits".** Profile F's best match scored only 0.52, but the list looked as confident as any other.
- **Profile E's results were nearly tied (0.67–0.72).** With nothing to match on, the order was close to arbitrary.
- **Profile D got split results.** One song matched the "sad" half. The rest matched only the "loud" half.

**Comparing each pair of profiles**

- **A vs B:** no songs in common. A wants loud, bright, electronic songs, and B wants quiet, acoustic ones, so the lists are opposites, which is right.
- **A vs C:** *Gym Hero*, *Pulse Cathedral* and *Storm Runner* appear in both. Both listeners want loud songs with little acoustic sound. They differ on mood: A gets happy songs (*Sunrise City*, *Rooftop Lights*) and C gets darker ones (*Iron Requiem*, *Concrete Verses*), because C's target for upbeat feel is much lower.
- **A vs D:** only *Storm Runner* is shared, and it is there for loudness only. D's other picks are slow and acoustic or loud and dark, which are the opposite of A's cheerful picks.
- **A vs E:** no overlap. E's middle-of-everything targets pull in medium-energy songs (r&b, country, reggae), and A only wants loud ones.
- **A vs F:** only *Sunrise City* overlaps, because it is bright and non-acoustic. F's zero-energy target removes the other loud pop songs.
- **B vs C:** no overlap. Calm acoustic lofi against loud rock is the cleanest opposite pair, and the lists reflect it.
- **B vs D:** no overlap, even though both like acoustic sound. D's loud target pulls its list toward metal and rock, and only its #1 (*Adagio for Rain*) is acoustic. That shows the energy target overpowering the acoustic one.
- **B vs E:** *Midnight Coding* and *Focus Flow* are shared. E's mid-range numbers sit close to those slow lofi songs, which makes sense.
- **B vs F:** no overlap, although both want quiet music. F also wants zero acoustic sound and maximum happiness, which rules out the acoustic lofi songs B loves, so "low energy" alone isn't enough to share a list.
- **C vs D:** *Iron Requiem* and *Storm Runner* are shared. Both want loud songs, so D's list is C's loud picks plus one sad classical piece. The result is valid, but it shows D only got half of what they asked for.
- **C vs E:** no overlap, because C wants extremes and E wants the middle.
- **C vs F:** only *Concrete Verses* is shared, a mid-energy, non-acoustic song. C wants energy 0.92 and F wants 0.0, so the two lists barely meet.
- **D vs E:** *Dust Road Home* is shared. It is a mid-energy country song, so it falls between D's two halves and in the middle of E's targets.
- **D vs F:** no overlap. Both are conflicting profiles, but they conflict in different ways, so they end up in different places.
- **E vs F:** *Velvet Hours* and *Island Sway* are shared. When nothing fits, both lists fall back on warm, mid-range songs, which shows that no-match users get similar default answers.

**Is the output valid?** For the standard profiles, yes. The changes between pairs follow the numbers each listener asked for, in ways that make sense. For the tricky profiles, the system does something reasonable but doesn't tell the user when it couldn't find a good match.

---

## 8. Future Work  

1. **Say "no good match".** If the best score is low, tell the user. Right now it always shows five confident-looking songs.  
2. **Give partial credit for similar labels.** "Indie pop" should earn something for a "pop" fan. "Relaxed" should earn something for "chill".  
3. **Grow the catalog.** Add more songs per genre. Then the top five would have real choices.  
4. **Mix up the top five.** Avoid five near-copies of the same song.  
5. **Handle mixed tastes.** Let a user list two moods or two genres, so "sad but energetic" has a better answer.  

---

## 9. Personal Reflection  

I learned that a recommender is just a set of rules and weights. The weights are choices a person makes in this case. A small change, like doubling the energy weight, moved songs around and changed who was served well.  

The surprise was *Gym Hero*. It kept showing up for happy pop fans. It was not a bug. The song sounded right, and the mood label was worth too little to stop it.  

I also learned that tricky test profiles teach more than normal ones. They showed where the system breaks.  

Now I think differently about music apps. A "personal" list can hide the fact that the system had little to choose from. It may just be guessing, especially if there's limited data.  

**My biggest learning moment.** It was seeing that the weights are choices. I thought the formula was the answer. Then I doubled one number and the rankings changed. That decision is where bias comes from.  

**How AI helped, and when I double-checked it.**  

- AI helped me write the loader, the scoring and the ranking fast. It also helped me draft the docs and plan the test profiles. 
- I still had to check its work. The AI's first recipe used different weights than my README. I had to pick one and make them match.
- One test run showed old results after I reverted a change. The cause was cached files. I only caught it because I compared the output to a saved copy.  
- The AI claimed a "working recommender". That was only partly true. The `Recommender` class is still a placeholder.  
- An example in the assignment said "60% of the data is pop". I counted, and only 2 of 18 songs are pop.

**What surprised me.** A simple sum of a few numbers still felt like a real recommendation. Sunrise City came first for a happy pop fan, which seemed right. The reason list made it feel even smarter. But the same rules also gave a confident list to a listener it could not help. Feeling right and being right are not the same thing.

**What I would try next.**  

- Add a "no good match" warning.  
- Give partial credit to similar genres and moods.  
- Use a bigger catalog.  
- Try tempo and danceability, which the model ignores now.  
- Let a listener give two moods, so mixed tastes work better.  