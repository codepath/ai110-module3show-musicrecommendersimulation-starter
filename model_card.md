# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

A small recommender that picks songs by genre, mood and energy.

---

## 2. Intended Use  

**What it does.** It suggests 5 songs from a list of 20. You give it a favorite genre, a favorite mood and an energy level. It scores every song and shows the top 5. It also shows why each song was picked.

**What it assumes about you.**

- You know your favorite genre and mood.
- One word each is enough to describe them.
- Your energy taste is one number from 0 (calm) to 1 (intense).
- Your taste stays the same all the time.

**Who it is for.** It is for classroom learning only. It is not for real listeners. The song list is too small, and the system is too simple.

---

## 3. How the Model Works  

Think of the recommender as a judge. It gives every song a score out of 4. Then it shows you the top 5.

**What it knows about you.** You tell it three things:

- Your favorite genre.
- Your favorite mood.
- How much energy you want, from 0 (calm) to 1 (intense).

**What it looks at in each song.** Only genre, mood and energy. The data also has tempo, valence, danceability and acousticness. The score does not use them.

**How the points work.**

- **Genre: 1 point** if it matches your favorite. Otherwise 0.
- **Mood: 1 point** if it matches your favorite. Otherwise 0.
- **Energy: up to 2 points.** The closer a song is to your energy, the more points it gets. A song that is too loud loses points. A song that is too quiet loses points too.

If you pick an energy below 0 or above 1, it counts as 0 or 1. So energy points never go below zero.

**Why energy is worth the most.** At first, genre was worth 2 points. Then a metal fan who wanted quiet music got the loudest metal song first. That was wrong. I gave energy more points and it got fixed.

**How the list is made.** The judge scores every song. It sorts them from highest to lowest. It shows the top 5 and the reasons for each score.

**An example.** Say you want pop, happy and energy 0.9.

- Sunrise City (pop, happy, 0.82) scores 3.84. It gets 1 for genre, 1 for mood and 1.84 for energy.
- Gym Hero (pop, intense, 0.93) scores 2.94. It gets 1 for genre and 1.94 for energy. It gets no mood point.

**What I changed from the starter code.** The starter had empty functions. I filled them in. I added the reasons and a cleaner printout. I first used 2 points for genre, 1 for mood and 1 for energy. After testing, I changed it to 1, 1 and 2. These numbers are my choice. They are not proven best.

**Blind spots.**

- Genre and mood must match exactly. Indie pop gets no credit for a pop fan.
- Energy counts the most. So a loud song in the wrong genre can beat a quiet song in the right genre.

---

## 4. Data  

**Size.** The catalog is in `data/songs.csv`. It has 20 songs by 18 artists. The starter file had 10 songs. I added 10 more.

**What each song has.** A title, an artist, a genre, a mood, and five numbers: energy, tempo, valence, danceability and acousticness. The score only uses genre, mood and energy.

**Genres and moods.** There are 17 genres and 16 moods. Lofi has 3 songs and pop has 2. The other 15 genres have 1 song each.

**Energy.** Songs range from 0.22 to 0.97. No song falls between 0.55 and 0.75.

**What is missing.**

- There is no "sad" mood.
- There are no lyrics, languages or release years.
- There is no sense of how popular a song is.
- There is no way to tell a workout song from a party song.
- Most genres have only one song. So one song stands for a whole genre.

---

## 5. Strengths  

**Clear tastes in a well-covered genre work best.** The Chill Lofi listener got Library Rain first with a perfect 4.00. The next two songs were lofi too. That matched what I expected.

**Opposite tastes get opposite lists.** The pop and lofi lists share no songs. Pop gets loud songs and lofi gets quiet ones. That is right.

**Energy is scored fairly.** A song that is too loud and a song that is too quiet are both penalized. The system does not just push for more energy.

**The reasons are easy to read.** Every song shows how it got its points. That made it simple to find problems.

**The Deep Intense Rock list felt right.** Storm Runner came first. Loud songs filled the rest.

**The scoring math is safe.** I tested 880 scores. All of them stayed between 0 and 4. A perfect match scored exactly 4.

---

## 6. Limitations and Bias 

**Features it does not use.**

- Valence, tempo, danceability and acousticness are in the data but never scored.
- The `likes_acoustic` setting is dropped before scoring. Changing it changes nothing.
- So the system can't tell a happy song from an intense one by how it feels. It only reads the label.

**Genres and moods that are underrepresented.**

- 15 of 17 genres have only one song.
- No song has the mood "sad".
- No song has energy between 0.55 and 0.75.
- The quietest song is 0.22.

**Where it leans too hard on one thing.**

- Energy is worth the most. A loud song in the wrong genre can beat a quiet song in the right genre.
- Genre and mood must match exactly. "indie pop" does not match "pop". "Pop" with a capital letter matches nothing.
- Gym Hero shows up for 5 of my 9 profiles. It is pop, it is loud, and its mood is "intense".

**Who the scoring quietly favors.**

- Lofi and pop fans get more genre matches than anyone else.
- A listener who wants energy 0.0 can earn at most 1.56 of the 2.0 energy points. No song is that quiet.
- Mid-energy listeners get almost no ranking signal. At a target of 0.65 the top 5 scores are 1.74 to 1.80. The order is close to random.
- Typos and unknown genres give normal-looking lists. The system never says it found no match.

---

## 7. Evaluation  

I tested nine made-up listeners. I looked at whether each top 5 matched what that person would want.

### Profiles I tested

Three are ordinary:

- **High-Energy Pop:** pop, happy, very energetic (0.9).
- **Chill Lofi:** lofi, chill, quiet (0.35).
- **Deep Intense Rock:** rock, intense, very loud (0.95).

Six are tricky on purpose:

- **Sad but High Energy:** pop fan who wants a "sad" mood and high energy.
- **Genre-Only Trap:** metal fan who wants quiet, chill music.
- **Classical + Angry + Max Energy:** classical fan who wants angry, very loud music.
- **Out-of-Range Energy:** lofi fan with an energy of 2.0. The scale stops at 1.0.
- **Case Mismatch:** pop and happy fan who typed "Pop" and "Happy" with capital letters.
- **Unknown Genre and Mood:** wants "k-pop" and "sad" at middle energy. Neither exists in the song list.

### What surprised me

- **Gym Hero showed up everywhere.** It was in the top 5 for 5 of 9 profiles. It was #1 for the sad listener.
- **"Sad" changed almost nothing.** No song is labeled sad. The system ignored it and gave cheerful songs.
- **The ordinary profiles hid the problems.** All three looked fine. The tricky ones showed the weak spots.
- **Typos still gave good-looking lists.** The scores were around 1.9. But the lists only matched on loudness. The system never said it found no match.
- **Small weight changes changed the winner.** When I made energy count more, the metal fan finally got quiet songs.

### Why does Gym Hero keep showing up for people who want Happy Pop?

The system does not hear the music. It checks boxes.

Gym Hero is pop. It is also very loud. So it gets the genre point and almost all of the energy points. It only misses the mood. Its mood is "intense", not "happy". It scores 2.94 out of 4.

Sunrise City checks all three boxes. It scores 3.84. So it wins. Gym Hero is next because there are only two pop songs.

Think of a shop worker who hears "upbeat pop". They hand you the workout mix. It is pop and it is loud. But it does not feel happy. The system can't tell the difference. It only compares words.

Rock fans ask for "intense". Gym Hero is "intense" too. So it scores for them as well. That is why it is #2 for Deep Intense Rock.

Rooftop Lights is happy. But it is "indie pop", not "pop". The system sees those as different words. It scores only 2.72.

### Comparing pairs of profiles

There are 36 pairs. I compared the three ordinary profiles. Then I compared each tricky profile with the ordinary one it came from. Then I compared two pairs of tricky ones.

**The three ordinary profiles**

- **Pop vs. Lofi:** No shared songs. Pop gets loud songs. Lofi gets quiet songs. That is right.
- **Pop vs. Rock:** Both want loud music. Three songs overlap: Storm Runner, Gym Hero and Fuego en la Noche. The labels set the order. Rock gets Storm Runner first. Pop gets Sunrise City first.
- **Lofi vs. Rock:** No shared songs. Quiet and loud tastes get different lists. That is right.

**Each tricky profile vs. its ordinary twin**

- **Sad but High Energy vs. High-Energy Pop:** Only the mood is different. The same two songs lead both lists. There is no sad song to find. So the sad listener gets happy music.
- **Genre-Only Trap vs. Chill Lofi:** Four of five songs match. There is no quiet metal song. So the chill mood and low energy win. Iron Verdict, the only metal song, is gone. That is what I wanted.
- **Classical + Angry vs. Deep Intense Rock:** Same five loud songs, new order. "Angry" puts Iron Verdict first. The only classical song is very quiet, so it drops out. That fits "very loud". But it ignores "classical".
- **Out-of-Range Energy vs. Chill Lofi:** Both get the same two lofi songs first. Then the 2.0 listener gets loud songs. The system reads 2.0 as "as loud as possible". A lofi fan did not want that.
- **Case Mismatch vs. High-Energy Pop:** The capital letters cost every label point. Sunrise City is still first, but its score is 1.96, not 3.84. A hip hop song is #2. The list looks fine, but only loudness picked it.

**Tricky profiles with the same problem**

- **Genre-Only Trap vs. Classical + Angry:** Mirror images. In both, genre can't beat a big energy gap. The quiet metal fan gets quiet songs. The loud classical fan gets loud songs.
- **Case Mismatch vs. Unknown Genre and Mood:** Neither matches any label. Both lists use loudness only. Scores are all between 1.84 and 1.96. Neither list is what the listener asked for.

The other pairs work the same way. The lists share loud or quiet songs. Genre and mood only decide who is first.

### Terminal output per profile

Output of `python3 -m src.main` (top 5 per profile). The first three are typical listeners; the rest are adversarial profiles built to probe the scoring logic.

#### High-Energy Pop

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=pop, mood=happy, energy=0.9
Top 5 recommendations
----------------------------------------------------------------

#1  Sunrise City  by Neon Echo
    Score: 3.84 / 4.00
    Reasons:
      - genre match: pop (+1.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.90 (+1.84)

#2  Gym Hero  by Max Pulse
    Score: 2.94 / 4.00
    Reasons:
      - genre match: pop (+1.0)
      - energy 0.93 vs target 0.90 (+1.94)

#3  Rooftop Lights  by Indigo Parade
    Score: 2.72 / 4.00
    Reasons:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.90 (+1.72)

#4  Storm Runner  by Voltline
    Score: 1.98 / 4.00
    Reasons:
      - energy 0.91 vs target 0.90 (+1.98)

#5  Fuego en la Noche  by Luna Caliente
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.85 vs target 0.90 (+1.90)

================================================================
```

#### Chill Lofi

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=lofi, mood=chill, energy=0.35
Top 5 recommendations
----------------------------------------------------------------

#1  Library Rain  by Paper Lanterns
    Score: 4.00 / 4.00
    Reasons:
      - genre match: lofi (+1.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 0.35 (+2.00)

#2  Midnight Coding  by LoRoom
    Score: 3.86 / 4.00
    Reasons:
      - genre match: lofi (+1.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 0.35 (+1.86)

#3  Focus Flow  by LoRoom
    Score: 2.90 / 4.00
    Reasons:
      - genre match: lofi (+1.0)
      - energy 0.40 vs target 0.35 (+1.90)

#4  Spacewalk Thoughts  by Orbit Bloom
    Score: 2.86 / 4.00
    Reasons:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 0.35 (+1.86)

#5  Coffee Shop Stories  by Slow Stereo
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.37 vs target 0.35 (+1.96)

================================================================
```

#### Deep Intense Rock

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=rock, mood=intense, energy=0.95
Top 5 recommendations
----------------------------------------------------------------

#1  Storm Runner  by Voltline
    Score: 3.92 / 4.00
    Reasons:
      - genre match: rock (+1.0)
      - mood match: intense (+1.0)
      - energy 0.91 vs target 0.95 (+1.92)

#2  Gym Hero  by Max Pulse
    Score: 2.96 / 4.00
    Reasons:
      - mood match: intense (+1.0)
      - energy 0.93 vs target 0.95 (+1.96)

#3  Neon Overdrive  by Pulse Drift
    Score: 1.98 / 4.00
    Reasons:
      - energy 0.96 vs target 0.95 (+1.98)

#4  Iron Verdict  by Black Anvil
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.97 vs target 0.95 (+1.96)

#5  Fuego en la Noche  by Luna Caliente
    Score: 1.80 / 4.00
    Reasons:
      - energy 0.85 vs target 0.95 (+1.80)

================================================================
```

#### Conflicting: Sad but High Energy

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=pop, mood=sad, energy=0.9
Top 5 recommendations
----------------------------------------------------------------

#1  Gym Hero  by Max Pulse
    Score: 2.94 / 4.00
    Reasons:
      - genre match: pop (+1.0)
      - energy 0.93 vs target 0.90 (+1.94)

#2  Sunrise City  by Neon Echo
    Score: 2.84 / 4.00
    Reasons:
      - genre match: pop (+1.0)
      - energy 0.82 vs target 0.90 (+1.84)

#3  Storm Runner  by Voltline
    Score: 1.98 / 4.00
    Reasons:
      - energy 0.91 vs target 0.90 (+1.98)

#4  Fuego en la Noche  by Luna Caliente
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.85 vs target 0.90 (+1.90)

#5  Neon Overdrive  by Pulse Drift
    Score: 1.88 / 4.00
    Reasons:
      - energy 0.96 vs target 0.90 (+1.88)

================================================================
```

#### Genre-Only Trap (Metal, Chill, Low)

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=metal, mood=chill, energy=0.2
Top 5 recommendations
----------------------------------------------------------------

#1  Spacewalk Thoughts  by Orbit Bloom
    Score: 2.84 / 4.00
    Reasons:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 0.20 (+1.84)

#2  Library Rain  by Paper Lanterns
    Score: 2.70 / 4.00
    Reasons:
      - mood match: chill (+1.0)
      - energy 0.35 vs target 0.20 (+1.70)

#3  Midnight Coding  by LoRoom
    Score: 2.56 / 4.00
    Reasons:
      - mood match: chill (+1.0)
      - energy 0.42 vs target 0.20 (+1.56)

#4  Rainfall Nocturne  by Elara Voss
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.22 vs target 0.20 (+1.96)

#5  Coffee Shop Stories  by Slow Stereo
    Score: 1.66 / 4.00
    Reasons:
      - energy 0.37 vs target 0.20 (+1.66)

================================================================
```

#### Classical + Angry + Max Energy

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=classical, mood=angry, energy=1.0
Top 5 recommendations
----------------------------------------------------------------

#1  Iron Verdict  by Black Anvil
    Score: 2.94 / 4.00
    Reasons:
      - mood match: angry (+1.0)
      - energy 0.97 vs target 1.00 (+1.94)

#2  Neon Overdrive  by Pulse Drift
    Score: 1.92 / 4.00
    Reasons:
      - energy 0.96 vs target 1.00 (+1.92)

#3  Gym Hero  by Max Pulse
    Score: 1.86 / 4.00
    Reasons:
      - energy 0.93 vs target 1.00 (+1.86)

#4  Storm Runner  by Voltline
    Score: 1.82 / 4.00
    Reasons:
      - energy 0.91 vs target 1.00 (+1.82)

#5  Fuego en la Noche  by Luna Caliente
    Score: 1.70 / 4.00
    Reasons:
      - energy 0.85 vs target 1.00 (+1.70)

================================================================
```

#### Out-of-Range Energy (2.0)

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=lofi, mood=chill, energy=2.0
Top 5 recommendations
----------------------------------------------------------------

#1  Midnight Coding  by LoRoom
    Score: 2.84 / 4.00
    Reasons:
      - genre match: lofi (+1.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 1.00 (+0.84)

#2  Library Rain  by Paper Lanterns
    Score: 2.70 / 4.00
    Reasons:
      - genre match: lofi (+1.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 1.00 (+0.70)

#3  Iron Verdict  by Black Anvil
    Score: 1.94 / 4.00
    Reasons:
      - energy 0.97 vs target 1.00 (+1.94)

#4  Neon Overdrive  by Pulse Drift
    Score: 1.92 / 4.00
    Reasons:
      - energy 0.96 vs target 1.00 (+1.92)

#5  Gym Hero  by Max Pulse
    Score: 1.86 / 4.00
    Reasons:
      - energy 0.93 vs target 1.00 (+1.86)

================================================================
```

#### Case Mismatch (Pop/Happy)

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=Pop, mood=Happy, energy=0.8
Top 5 recommendations
----------------------------------------------------------------

#1  Sunrise City  by Neon Echo
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.82 vs target 0.80 (+1.96)

#2  Concrete Crown  by Kid Meridian
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.78 vs target 0.80 (+1.96)

#3  Rooftop Lights  by Indigo Parade
    Score: 1.92 / 4.00
    Reasons:
      - energy 0.76 vs target 0.80 (+1.92)

#4  Fuego en la Noche  by Luna Caliente
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.85 vs target 0.80 (+1.90)

#5  Night Drive Loop  by Neon Echo
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.75 vs target 0.80 (+1.90)

================================================================
```

#### Unknown Genre and Mood

```
================================================================
                       MUSIC RECOMMENDER                        
================================================================
Profile: genre=k-pop, mood=sad, energy=0.5
Top 5 recommendations
----------------------------------------------------------------

#1  Dusty Porch Swing  by Willow Creek
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.48 vs target 0.50 (+1.96)

#2  Velvet Hours  by Amara Sol
    Score: 1.96 / 4.00
    Reasons:
      - energy 0.52 vs target 0.50 (+1.96)

#3  Island Breeze  by Ziggy Tides
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.55 vs target 0.50 (+1.90)

#4  Smoke and Rain  by Delta Hollow
    Score: 1.90 / 4.00
    Reasons:
      - energy 0.45 vs target 0.50 (+1.90)

#5  Midnight Coding  by LoRoom
    Score: 1.84 / 4.00
    Reasons:
      - energy 0.42 vs target 0.50 (+1.84)

================================================================
```

---

## 8. Future Work  

- **Use the unused data.** Make `likes_acoustic` change the score. Add valence so "happy" and "sad" can be judged by feel. That would fix Storm Runner showing up for a happy fan.
- **Make labels forgiving.** Ignore capital letters. Give partial credit to close moods, like sad and melancholy.
- **Say when nothing matches.** Warn the user if their genre or mood is not in the list.
- **Add variety.** Allow only two songs per artist in the top 5. Add one surprise song.
- **Fix the song list.** Add songs with energy 0.55 to 0.75. Add songs below 0.2. Add more songs per genre.
- **Allow richer tastes.** Let users pick more than one genre. Let them pick an energy range.
- **Try the experiments I skipped.** Remove the mood check and see what changes. Add tempo to the score.

---

## 9. Personal Reflection  

**My biggest learning moment.** I learned that a recommender is a set of choices. I changed two weights and the top song changed for two of my nine profiles. The data did not change. The metal fan who wanted quiet music got a loud metal song first. That showed me how much one number can decide.

**How AI helped, and when I double-checked it.** AI helped me move fast. It built the test profiles, ran the experiments and found a bug I had missed. The `likes_acoustic` setting was never used in scoring. It also helped me see problems, like the missing "sad" songs and the gap in energy.

But I had to check its work.

- I did not trust "the math is fine." We tested 880 scores. We checked that none went below 0 or above 4.
- I compared the results to my own ear. The lists looked right at the top. The lower picks, like Storm Runner for a happy pop fan, felt off.
- After I changed the weights, the README and model card were out of date. They still showed the old scores and the old "genre counts twice" text. I had to refresh them.
- Some claims were only read from the code and not measured. One example is that ties go to the song listed first. I would test those before relying on them.

**What surprised me about simple algorithms.** The system only adds three small scores. Yet the lists felt like real recommendations. The Chill Lofi list felt right. That is because the labels and the energy number happen to line up with how people think about music. It also fooled me when it was wrong. A typo still gave five songs with normal scores. Nothing said it had failed. A simple system can look smart without understanding anything.

**What I would try next.**

- Make `likes_acoustic` change the score.
- Add valence, so "happy" and "sad" are judged by feel.
- Ignore capital letters, and warn when no song matches.
- Limit each artist to two songs in the top 5.
- Add songs with energy 0.55 to 0.75, and more songs per genre.
- Try the experiments I skipped. Remove the mood check. Add tempo to the score.
