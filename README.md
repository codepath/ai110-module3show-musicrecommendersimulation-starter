# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a small content-based music recommender that suggests songs based on a user’s taste profile. The system compares song attributes like genre, mood, energy, and acousticness to what the user prefers, then assigns each song a score. After scoring all songs, it ranks them from highest to lowest and returns the top recommendations. The goal is to show how recommendation systems can turn user preferences and item features into predictions in a simple and explainable way.

---

## How The System Works

This recommender uses a content-based approach, meaning it recommends songs by comparing a user’s preferences directly to the features of each song in the catalog. Instead of learning from many users’ listening behavior, this version focuses on matching song attributes like genre, mood, energy, and acousticness. The goal is to build a simple and explainable system that shows how recommendation logic can be turned into code.

Each `Song` in the dataset includes attributes such as `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. For scoring, my system mainly uses `genre`, `mood`, `energy`, and `acousticness`. The `UserProfile` stores a favorite genre, a favorite mood, a target energy level, and whether the user prefers acoustic songs. This gives the recommender enough information to tell apart different types of listeners, such as someone who likes chill lofi versus someone who prefers intense rock.

### Features Used

**Song**
- genre
- mood
- energy
- acousticness

**UserProfile**
- favorite_genre
- favorite_mood
- target_energy
- likes_acoustic

### Example User Profile

```python
{
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4,
    "likes_acoustic": True
}
```

### Algorithm Recipe

My recommender uses a weighted scoring system to decide which songs to recommend.

For each song:
- add **+2.0 points** if the song’s genre matches the user’s favorite genre
- add **+1.5 points** if the song’s mood matches the user’s favorite mood
- add up to **+2.0 points** based on how close the song’s energy is to the user’s target energy
- add up to **+1.0 point** based on whether the song matches the user’s acoustic preference

After scoring every song in the dataset, the system sorts the songs from highest score to lowest score and returns the top 5 recommendations.

### Data Flow

Input: User preferences  
Process: Loop through every song in `songs.csv`, compute a score using the scoring logic, and save the result  
Output: Rank all songs by score and return the top recommendations

```mermaid
flowchart LR
    A[User Profile] --> B[Read songs from songs.csv]
    B --> C[Score each song]
    A --> C
    C --> D[Rank songs by score]
    D --> E[Return Top 5 recommendations]
```
    
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

## Experiments You Tried

I experimented with changing the weights used in the scoring system to see how the recommendations shifted. When genre was weighted more heavily, the recommender became stricter and mostly returned songs from the exact preferred genre, even if other songs matched the user’s mood and energy well. When mood or energy mattered more, the system produced recommendations that felt more flexible and vibe-based instead of being tied mainly to genre labels.

I also thought about adding features such as tempo and valence to make the scoring more detailed. This could help the system better distinguish between songs that share the same genre but feel very different. At the same time, adding too many features could make the scoring harder to explain and easier to overfit to small differences in the dataset.

---

## Evaluation

### User Profiles Tested

I tested two user profiles:

- User 1: prefers pop, happy mood, high energy
- User 2: prefers lofi, chill mood, low energy, acoustic songs

### Why the Top Song Ranked First

For User 2, “Library Rain” ranked first because it matched both the user’s preferred genre (“lofi”) and mood (“chill”), which have the highest weights in the scoring system. It also had an energy level very close to the user’s target (difference of 0.05), and it matched the user’s preference for acoustic songs.

### Comparison Between Users

The recommendations for User 2 are noticeably different from User 1. While User 1 received more energetic and upbeat songs, User 2 received calmer, more acoustic and chill songs. This shows that the recommender successfully adapts to different user preferences.

### Limitations and Bias

One limitation of this recommender is that it strongly prioritizes exact genre and mood matches. Songs that are similar but not labeled the same may be ranked lower, reducing diversity.

### Observations

One interesting observation is that some songs ranked lower even though they had very close energy levels. This shows that genre and mood have stronger influence on the final score.

---

## Limitations and Risks

This recommender only works on a very small catalog, so the recommendations are limited by what is available in the dataset. It does not understand lyrics, artist similarity, language, cultural context, or listening history, which means it misses many factors that shape real music preferences. It may also over-favor certain genres or moods depending on how the scoring weights are chosen. Because the rules are hand-designed, the system reflects human assumptions and may not generalize well to every listener.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

---

## Instruction Summary

This project is mainly about helping students understand how a simple recommender system turns user preferences into ranked results.

### Key ideas students should understand
- The recommender uses a **content-based approach**, meaning it compares user preferences directly to song features.
- Songs are scored using a **weighted scoring system**.
- Higher scores come from stronger matches in features such as genre, mood, energy, and acousticness.
- After scoring, songs are **sorted from highest to lowest** and the top results are returned.

### Most important implementation pieces
- `load_songs()` reads the dataset and converts each row into usable song data.
- `recommend_songs()` scores every song and returns the top ranked results.
- `Recommender.recommend()` does the same idea in the OOP version used by the tests.
- `explain_recommendation()` gives a short explanation for why a song ranked well.

### Where students may struggle
- Understanding how the weighted scoring formula works
- Seeing why one feature can affect ranking more than another
- Tracing how user preferences change the final output
- Understanding why exact genre or mood matches can dominate results

### What to emphasize when guiding students
- Focus on the idea that the recommender is just **assigning points and sorting**
- Encourage students to manually reason through why one song should rank above another
- Have students test at least two user profiles and compare the results
- Remind students that recommendation systems can still show bias even when the code is simple

### Common limitations to discuss
- The dataset is small, so recommendations are limited
- The system does not use listening history, lyrics, or artist similarity
- Exact category matching may reduce recommendation diversity
- Weight choices strongly affect outcomes


