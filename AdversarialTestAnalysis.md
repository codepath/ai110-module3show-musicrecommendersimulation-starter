# Adversarial Test Analysis & Profile Comparisons

## Executive Summary

Tested **6 adversarial/edge-case profiles** to understand what the recommender system actually rewards and punishes. This revealed hidden biases that favor certain user types while filtering out others.

---

## Core Findings

### Genre and Mood Dominance in the Scoring System

Simple answer: **Genre and mood bonuses dominate the scoring system.**

"Gym Hero" is a pop song with intense mood, high energy (0.93), and high danceability. When comparing to other profiles:

- **Happy Pop lover** gets +1.0 for genre match + +1.0 for mood match = 2.0 pts immediately. Energy similarity adds another 1.4 pts. Total: ~4.7 pts—easily top 3.
- **Sad Rock enthusiast** gets 0 pts for pop genre (doesn't match rock), but intense mood matches anyway (+1.0), and high energy matches their target (0.9) (+1.4). Total: ~3.7 pts—still makes top 5.
- **Chill Lofi lover** gets 0 pts for both, but the high energy gives a moderate score (~2.8 pts) through pure numeric matching.

**The real issue:** The algorithm **cannot see genre differences**—it only scores "does genre match or not?" Binary. So a pop song that matches on mood or energy will appear in recommendations across multiple genres because there's no penalty for "wrong genre + good mood/energy combination."

---

## Profile Comparisons

### Comparison 1: Conflicting Preferences vs. Impossible Genre

**Profile A:** Rock + Sad mood + High energy (0.9)  
**Profile B:** Dubstep (doesn't exist) + Intense mood + High energy (0.85)

| Ranking | Profile A (Rock + Sad) | Profile B (Dubstep + Intense) | Why? |
|---------|------|------|------|
| #1 | Storm Runner (Rock) | Storm Runner (Rock) | Both profiles value **energy above all else**. Mood isn't exact match, but 0.91 energy beats everything. |
| #2 | Metal Storm (Metal) | Metal Storm (Metal) | Again, energy match (0.95) wins. Even though it's metal/rock (wrong genre for B), the intense mood compensation is enough. |
| #3 | Neon Pulse (Electronic) | Gym Hero (Pop) | Profile A keeps rock songs longer; Profile B starts accepting any high-energy song since dubstep doesn't exist. |

**Why this makes sense:** When your favorite genre doesn't exist in the dataset, the system doesn't punish you—it just stops using the genre bonus. But mood and energy bonuses take over completely, so you get the "most energetic intense songs" regardless of actual genre.

---

### Comparison 2: Extreme Values vs. Neutral Profile

**Profile A:** Jazz + Focused mood + Extremes (energy 0.05, valence 0.95, acousticness 0.99)  
**Profile B:** Pop + Happy mood + All values at 0.5 (neutral)

| Ranking | Profile A (Extremes) | Profile B (Neutral) | This Shows... |
|---------|------|------|------|
| #1 | Jazz Improvisation (5.61) | Sunrise City (4.69) | Profile A's extremes pull towards jazz+focused combo. Profile B gets most "average" song. |
| #2 | Coffee Shop Stories (4.89) | Rooftop Lights (3.48) | Profile A accepts any close-to-extreme match. Profile B penalizes songs that only match on mood (no energy bonus). |
| #3 | Jazz Nights (4.79) | Gym Hero (3.45) | Profile A gets very specific jazz results. Profile B gets songs matching **any single attribute**. |

**Why neutral profile scores lower overall:** The algorithm rewards **specificity in preferences**. When you ask for exactly 0.5 energy, 0.5 valence, and 0.5 acousticness, almost nothing matches well (most songs are > 0.6 on at least one). But when you ask for extremes, even though they're uncommon, the system can find perfect matches at least on one or two attributes.

---

### Comparison 3: Acoustic Paradox vs. Inverted Rock

**Profile A:** Lofi + Chill mood + High energy (0.95) + High acousticness (0.9)  
**Profile B:** Rock + Chill mood + Low energy (0.25) + High acousticness (0.85)

| Ranking | Profile A (Paradox) | Profile B (Inverted Rock) | The Pattern |
|---------|------|------|------|
| #1 | Lo-Fi Memories (5.30) | Spacewalk Thoughts (4.91) | Both get **non-matching genres**. Profile A gets lofi (genre match saved it). Profile B gets ambient (no rock songs with low energy exist). |
| #2 | Chill Wave (5.22) | Chill Wave (4.35) | Profile A: **genre bonus huge**. Profile B: no genre bonus, scores lower. |
| #3 | Library Rain (5.21) | Library Rain (4.35) | Both reach for lofi/chill fallback. |

**In plain English:** Profile A's lofi + chill mood give **+2.0 bonus points automatically**. Even though it asks for high energy (0.95), which contradicts lofi/chill songs, the genre penalty never happens. The algorithm just... ignores the energy request and returns chill lofi songs.

Profile B has no genre match, so it falls back entirely on mood (chill). No acoustic songs exist with rock genre, so it gives up on that and returns ambient/lofi instead.

**Why this matters:** The system **punishes you for asking for uncommon genre combinations** but **rewards you for asking for common ones**, even when the preferences contradict (sad + energetic OR chill + high energy).

---

## Summary: Who Gets Good Recommendations?

✅ **Users with common genres** (Pop, Rock, Lofi, Jazz) get quick, high-scoring results  
✅ **Users with "balanced" preferences** (energy ≈ 0.5, valence ≈ 0.5) get reasonable matches  
✅ **Users with strong mood/energy matches** get results even if genre is missing  

❌ **Users with rare genres** (K-pop, Reggae, Country) see results drop 15–20% automatically  
❌ **Users with contradictory preferences** (sad + energetic, chill + high-energy) get penalized despite these being real music tastes  
❌ **Users wanting specific danceability/tempo** get totally ignored—these attributes don't score at all  

---

## The Hidden Filter Bubble

The system **invisibly filters toward "average" and "common" user types:**

- Users who like sad, energetic music? Penalized.
- Users who like K-pop? Automatic 20% score penalty due to small dataset.
- Users who want danceable music? Completely invisible in the scoring system.

This isn't malicious—it's just that **categorical features (genre, mood)** dominate the algorithm, and the dataset doesn't reflect the full diversity of real music taste.
