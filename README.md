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

How i I understand real world recommenders work is that they will use collaborative filtering to look at patterns across the users behaviors and content based filtering to look at the actual attributes to the songs. In my user behavior patterns.

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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

=======================================================
  TOP SONG RECOMMENDATIONS
=======================================================

1. Sunrise City — Neon Echo
   Score: 5.46
   Why:   genre match (pop) (+2.0); mood match (happy) (+1.5); energy closeness (0.82 vs target 0.80) (+1.96)

2. Gym Hero — Max Pulse
   Score: 3.74
   Why:   genre match (pop) (+2.0); energy closeness (0.93 vs target 0.80) (+1.74)

3. Rooftop Lights — Indigo Parade
   Score: 3.42
   Why:   mood match (happy) (+1.5); energy closeness (0.76 vs target 0.80) (+1.92)

4. Night Drive Loop — Neon Echo
   Score: 1.90
   Why:   energy closeness (0.75 vs target 0.80) (+1.90)

5. Storm Runner — Voltline
   Score: 1.78
   Why:   energy closeness (0.91 vs target 0.80) (+1.78)

=======================================================

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

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



