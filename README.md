# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two signals. Collaborative filtering learns from the behavior of millions of users ("people like you also liked this"), and content-based filtering compares the attributes of the songs themselves. This simulation is content-based only. It has no listening history from other users, so it compares each song's attributes to one user's stated taste. It scores each song on the user's preferred **genre**, **mood**, and **energy**.

### Song features

Each `Song` stores:

- `genre` and `mood` (categories)
- `energy`, `valence`, `danceability`, `acousticness` (0.0 to 1.0)
- `tempo_bpm` (beats per minute)
- `id`, `title`, `artist` (identifying info, not used for scoring)

### UserProfile features

Each `UserProfile` stores:

- `favorite_genre`
- `favorite_mood`
- `target_energy` (0.0 to 1.0)
- `likes_acoustic` (True or False)

### How a song is scored

Each song gets a score from 0 to 4.0 by adding up three parts:

- **Genre:** +1.0 if the song's genre matches the user's favorite genre, otherwise 0.
- **Mood:** +1.0 if the song's mood matches the user's favorite mood, otherwise 0.
- **Energy:** up to +2.0 based on how close the song is to `target_energy`, using `2.0 * (1 - |song energy - target energy|)`. `target_energy` is clamped to 0.0–1.0 first, so the energy part never goes negative. A song is not rewarded for simply having more energy.

Genre and mood are weighted equally, and energy is worth the most (up to twice either label). A song with the right energy and no label matches (up to 2.0) can beat a song that matches one label but has the wrong energy. Genre alone no longer outweighs a large energy mismatch.

### Ranking modes

You can change how much each part of the score is worth. There are three modes. Each one adds up to 4.0.

| Mode | Genre | Mood | Energy |
|---|---|---|---|
| `genre-first` | 2.0 | 1.0 | 1.0 |
| `mood-first` | 1.0 | 2.0 | 1.0 |
| `energy-focused` (default) | 1.0 | 1.0 | 2.0 |

```
python3 -m src.main                      # default mode
python3 -m src.main --mode mood-first    # pick a mode
python3 -m src.main --mode all           # run every mode
python3 -m src.main --profile rock       # only profiles with "rock" in the name
```

In code, pass a strategy: `recommend_songs(prefs, songs, strategy=MOOD_FIRST)`.

### How songs are chosen

The `Recommender` scores every song in the catalog, sorts them from highest to lowest score, and returns the top `k` (5 by default). Each result includes a short explanation of why it was picked.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python3 -m src.main` runs the recommender for three typical profiles and six adversarial/edge-case profiles, printing the top 5 results for each.

### High-Energy Pop

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

### Chill Lofi

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

### Deep Intense Rock

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

### Conflicting: Sad but High Energy

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

### Genre-Only Trap (Metal, Chill, Low)

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

### Classical + Angry + Max Energy

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

### Out-of-Range Energy (2.0)

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

### Case Mismatch (Pop/Happy)

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

### Unknown Genre and Mood

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**1. Nine user profiles.** Three were ordinary: High-Energy Pop, Chill Lofi and Deep Intense Rock. They gave good lists. Six were tricky on purpose. They showed problems:

- A "sad" request got cheerful songs. No song is labeled sad.
- A metal fan who wanted quiet music got a loud metal song first.
- Capital letters ("Pop") or an unknown genre ("k-pop") gave lists sorted by loudness only.
- Gym Hero was in the top 5 for 5 of the 9 profiles.

All nine outputs are shown above.

**2. Weight shift.** I changed genre from 2.0 to 1.0. I changed energy from 1.0 to 2.0. Mood stayed at 1.0. The top score is still 4.0.

The three ordinary profiles did not change. Two tricky profiles got a better #1 song:

| Profile | Old #1 | New #1 |
|---|---|---|
| Genre-Only Trap (metal, chill, 0.2) | Iron Verdict (loud metal, 0.97) | Spacewalk Thoughts (quiet ambient, 0.28) |
| Classical + Angry + 1.0 | Rainfall Nocturne (quiet classical, 0.22) | Iron Verdict (loud, angry) |

So the genre weight matters a lot when a user's wishes conflict. It matters little when they agree. I kept the new weights.

**3. Clamping energy to 0–1.** After doubling energy, an energy of 2.0 gave negative points. One top-5 song scored below zero. Clamping fixed it.

I then tested the math with 880 scores. I used extreme energies, odd genre text and all 20 songs. Every score stayed between 0 and 4. A perfect match scored exactly 4.0. The two existing tests still passed.

**4. A bias check across the song list.** I ran 399 recommendations. I used every genre and mood pair at 21 energy levels.

- Every song could show up.
- Songs in the busy low-energy group showed up about 3 times more than songs at the edges. Library Rain showed up 189 times. Wildflower Road showed up 54 times.
- A listener who wants energy 0.0 can earn at most 1.56 of 2.0 energy points. The quietest song is 0.22.
- The `likes_acoustic` setting is never used in scoring.

**Not tried yet.** Adding tempo or valence to the score. Removing the mood check.

---

## Limitations and Risks

- **Tiny song list.** There are only 20 songs. 15 of the 17 genres have one song. A listener with a rare taste gets one genre match. The rest are picked by energy only.
- **Uneven energy.** No song has energy between 0.55 and 0.75. The quietest is 0.22. Some listeners get weaker matches.
- **Exact-match labels.** "indie pop" gets nothing for a pop fan. "Pop" with a capital letter matches nothing. A mood like "sad" is ignored if it is not in the list.
- **Unused data.** Valence, tempo, danceability and acousticness are never scored. The `likes_acoustic` setting is dropped. That is why Gym Hero keeps showing up for happy pop fans.
- **No variety.** The result is the same every time. One artist can take two of the five slots.
- **No input checks.** Typos and unknown genres give normal-looking lists. There is no warning. Only energy is clamped.
- **No lyrics, language or sound.** The system does not know what a song sounds like.

The model card has more detail.

---

## Reflection

Full write-up:

[**Model Card**](model_card.md)

A recommender turns data into guesses. It compares what a user says to the labels and numbers on each song. It adds up points and sorts the songs. I learned that I make many of the choices by hand. Changing two weights changed the top song for two of my test profiles. Also, the lists looked fine even when the system misread the request. A score of 1.9 out of 4 looked normal. But it only measured loudness.

Bias showed up in places I did not expect. It was not mostly about which genre was favored. It came from the song list. No songs fall between 0.55 and 0.75 energy, and none are quieter than 0.22. It came from exact-match labels. "indie pop" and "pop" count as different words. It also came from data the system never uses. People with rare genres, odd moods or ignored settings get worse lists. Nothing tells them. A real app should say when it can't find a match. It should also be tested on unusual listeners, not just typical ones.
