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

My Short Paragraph: The idea of real-world recommendations incorporate many factors into ensuring the user's experience is to get them to enter in a flow state, which is to enjoy the music at all times. Thus, companies such as YouTube or Spotify are using different types of filtering and analyzing different behaviors to provide each user the right recommendations, which is providing predictions on what music they are likely to listen and enjoy next. Additionally, my version of a music recommender is the user to experience their musical 'vibe', which is to have the recommender find songs that create a similar emotional atmosphere and listening feel. 

Song Objects
- Mood
- Energy
- Valence
- Acousticness
- Tempo_BPM
- Genre

UserProfile Objects
- Musical Vibe
- Music Playlists
- Listening History
- Personal Registration Details (Email, DOB, Linked Social Accounts)

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
Loading songs from data/songs.csv...
Loaded songs: 18

Top recommendations:

1. Sunrise City by Neon Echo
   Score: 4.48
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.98)

2. Gym Hero by Max Pulse
   Score: 2.87
   Reasons:
     • genre match (+2.0)
     • energy closeness (+0.87)

3. Rooftop Lights by Indigo Parade
   Score: 2.46
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.96)

4. Beat Drop Thunder by Urban Collective
   Score: 0.95
   Reasons:
     • energy closeness (+0.95)

5. Night Drive Loop by Neon Echo
   Score: 0.95
   Reasons:
     • energy closeness (+0.95)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Algorithm Recipe and Expected Biases

My finalized recommendation recipe uses a simple weighted scoring system to rank songs for a user profile:

1. Start with the user's preferred genre and mood as the strongest signals.
2. Compare each candidate song to those preferences and give the highest weight to genre and mood matches.
3. Add a secondary score based on energy level so songs that are closer to the user's target energy are favored.
4. Use acousticness as a smaller tie-breaker for users who prefer more acoustic or less produced sounds.
5. Combine these signals into a single score and return the top recommendations with a short explanation.

A simplified version of the scoring rule looks like this: score = 0.4 × genre match + 0.3 × mood match + 0.2 × energy match + 0.1 × acousticness match.

I expect a few biases in this approach. Because the system is based on a small, hand-built music catalog, it may over-represent certain genres or moods that are more common in the dataset. It may also favor songs that fit a narrow idea of the "right" energy level and overlook more varied or surprising recommendations. In real-world recommenders, these kinds of biases can make the system feel repetitive or less fair to users with different tastes.

## Terminal Output for each Profile's recommendations

- Fenced Code Block #1

Loading songs from data/songs.csv...
Loaded songs: 18

Profile: High-Energy Pop
1. Sunrise City by Neon Echo
   Score: 4.48
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.98)

2. Gym Hero by Max Pulse
   Score: 2.87
   Reasons:
     • genre match (+2.0)
     • energy closeness (+0.87)

3. Rooftop Lights by Indigo Parade
   Score: 2.46
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.96)

- Fenced Code Block #2

Profile: Chill Lofi
1. Library Rain by Paper Lanterns
   Score: 4.88
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.95)
     • acoustic bonus (+0.43)

2. Midnight Coding by LoRoom
   Score: 4.84
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.98)
     • acoustic bonus (+0.35)

3. Focus Flow by LoRoom
   Score: 3.39
   Reasons:
     • genre match (+2.0)
     • energy closeness (+1.00)
     • acoustic bonus (+0.39)

- Fenced Code Block #3

Profile: Deep Intense Rock
1. Storm Runner by Voltline
   Score: 4.49
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.99)

2. Gym Hero by Max Pulse
   Score: 2.47
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.97)

3. Metal Fury by Thunder Strike
   Score: 2.46
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.96)

- Fenced Code Block #4

Profile: Conflicting Mood-Energy
1. Gym Hero by Max Pulse
   Score: 2.97
   Reasons:
     • genre match (+2.0)
     • energy closeness (+0.97)

2. Sunrise City by Neon Echo
   Score: 2.92
   Reasons:
     • genre match (+2.0)
     • energy closeness (+0.92)

3. Sad Blues by Mississippi Blues
   Score: 1.96
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.46)

- Fenced Code Block #5

Profile: No Match Fallback
1. Autumn Memories by Country Roads
   Score: 4.22
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.72)

2. Spacewalk Thoughts by Orbit Bloom
   Score: 0.92
   Reasons:
     • energy closeness (+0.92)

3. Moonlight Sonata by Classical Dream
   Score: 0.88
   Reasons:
     • energy closeness (+0.88)

- Fenced Code Block #6

Profile: Acoustic Bonus Trap
1. Storm Runner by Voltline
   Score: 3.84
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.29)
     • acoustic bonus (+0.05)

2. Gym Hero by Max Pulse
   Score: 1.79
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.27)
     • acoustic bonus (+0.03)

3. Metal Fury by Thunder Strike
   Score: 1.79
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.26)
     • acoustic bonus (+0.03)

- Top 3 Results in my Terminal Output Code Block

Top recommendations:

1. Storm Runner by Voltline
   Score: 3.84
   Reasons:
     • genre match (+2.0)
     • mood match (+1.5)
     • energy closeness (+0.29)
     • acoustic bonus (+0.05)

2. Gym Hero by Max Pulse
   Score: 1.79
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.27)
     • acoustic bonus (+0.03)

3. Metal Fury by Thunder Strike
   Score: 1.79
   Reasons:
     • mood match (+1.5)
     • energy closeness (+0.26)
     • acoustic bonus (+0.03)

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



