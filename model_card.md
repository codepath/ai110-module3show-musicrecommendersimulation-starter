# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**

It matches songs to the mood, genre, and energy you ask for.

---

## 2. Intended Use  

**Goal / task.** You give the model what you like: a genre, a mood, an energy
level, and whether you like acoustic sound. The model reads a small song
catalog and suggests the songs that fit you best. It also prints a short reason
for each pick.

**Who it is for.** This is a classroom project. It is for learning how a simple
recommender works, not for real listeners.

**What it assumes.** It assumes your taste can be described by a few tags. It
assumes the catalog has songs close to what you want.

**Intended use.**

- Exploring how scoring rules turn preferences into a ranked list.
- Testing how the system reacts to odd or conflicting requests.

**Not intended for.**

- Real music apps or real recommendations to real users.
- Any decision that matters. The catalog is tiny (18 songs).
- Judging an artist, a genre, or a person.

---

## 3. How the Model Works  

**Algorithm summary (in plain words).**

The model gives each song a score, then sorts by score. Points come from four
things:

- **Genre (worth the most).** Exact match gets full points. A close-sounding
  song gets partial points.
- **Mood (next).** Same idea: exact mood gets full points, a similar feel gets
  partial points.
- **Energy.** The closer the song's energy is to what you asked for, the more
  points it gets.
- **Acoustic sound (worth the least).** Points if the song matches whether you
  like acoustic or produced music.

"Close-sounding" is not guessed. The model measures how near a song is to the
average sound of that genre or mood in the catalog, using tempo, valence
(happy/sad feel), and danceability.

**What we changed from the starter logic.**

- If you type a word the catalog does not know (like "sad" or "k-pop"), the
  model maps it to a known word ("melancholic", "pop") so it still works.
- If it cannot honor a wish (like acoustic + loud EDM), it says so in a "note".
- It describes near matches honestly as a "similar sound", not a genre match.
- It shows a simple 0-to-10 score so numbers are easy to compare.
- It uses fitting words for the sound: "heavy" for rock/metal, "electronic"
  for pop/EDM.

---

## 4. Data  

**Size.** One CSV file with 18 songs.

**Features per song.** Title, artist, genre, mood, energy, tempo, valence,
danceability, and acousticness. Energy, valence, danceability, and
acousticness are 0-to-1 numbers. Tempo is beats per minute.

**Genres in the data.** pop, indie pop, lofi, rock, metal, EDM, synthwave,
hip hop, R&B, jazz, classical, reggae, country, folk, ambient.

**Moods in the data.** happy, chill, intense, focused, relaxed, moody,
energetic, melancholic, uplifting, aggressive, dark, nostalgic, romantic,
dreamy.

**Did we change it?** No. We did not add or remove songs.

**What is missing.** Most genres and moods have only one song. So "rock" or
"melancholic" is really just one track. There is no artist history, no lyrics,
no play counts, and no time or culture information. Many real genres (like
blues or afrobeat) are not here at all.

---

## 5. Strengths  

- **Clear requests work well.** A "high-energy pop" fan or a "chill lofi" fan
  gets songs that fit. The top picks look right.
- **It explains itself.** Every pick comes with a short reason.
- **It is honest.** If it cannot meet a wish, it says so in a note.
- **It handles new words.** Typing "sad" or "k-pop" still gives good results.
- **Near matches make sense.** For a rock fan, it surfaces metal and other
  heavy, high-energy tracks next.

---

## 6. Limitations and Bias 

**Observed behavior and biases.**

- **Thin data hurts sparse tags.** Only one song is "rock" and one is
  "melancholic". So the "average sound" for those tags is just that one song.
  Near-match scores for them are noisy.
- **Popular tags win.** Genres with more songs (like pop) match more often.
  Rare genres get fewer chances to show up.
- **Genre can dominate.** Genre is worth the most points. A user with a strong
  genre wish can crowd out other wishes.
- **Vague requests all look alike.** If you give almost nothing, the top list
  is nearly the same for everyone. Energy and acoustic sound decide it.
- **Unknown words still fail.** Known synonyms map fine, but a truly unknown
  word (like "polka") cannot be matched at all.
- **Explanations can repeat.** The same "note" can appear on every result.

---

## 7. Evaluation  

**Evaluation process.**

We tested by hand with user profiles, not with a metric.

- **Normal profiles.** Three clear listeners (high-energy pop, chill lofi, deep
  intense rock). We checked that the top picks made sense.
- **Adversarial profiles.** We built tricky profiles to try to break the
  scoring: conflicting wishes (high energy + sad), impossible wishes (acoustic
  + loud EDM), unknown words (k-pop, euphoric, polka), and near-empty inputs.
- **What we looked for.** Do the top picks fit? Are the reasons true? Does the
  system admit when it cannot meet a wish?
- **Before vs. after.** An early run found three problems. We fixed them and
  re-ran the same profiles to confirm the fixes held.
- **Unit tests.** Two small automated tests check that results come back sorted
  and that every pick has a non-empty explanation.

Full terminal output for every profile is below.

### Profiles tested

Three "normal" listener profiles plus a set of deliberately **adversarial /
edge-case** profiles (defined in `src/main.py`) were run against the 18-song
catalog. The adversarial set was designed to see whether the scoring logic can
be tricked or produce surprising results: conflicting energy/mood signals,
mutually exclusive preferences, out-of-vocabulary labels (recognized synonyms
*and* truly unknown ones), and near-empty profiles.

An earlier run surfaced three defects — unknown labels were silently dropped,
impossible preferences were never disclosed, and audio-only matches looked
broken with a flat low score. The output below is from the **revised** logic,
which (1) resolves out-of-vocabulary genre/mood through a synonym table onto
the catalog's real data-derived centroids, (2) discloses preferences a song
could not honor as a "note:", (3) describes fallback matches honestly as an
audio-profile match rather than a genre match, (4) shows a normalized `/10`
score that excludes unmatchable terms from the denominator, and (5) picks a
genre-appropriate word for the non-acoustic sound. Scores shown are
`raw (normalized/10)`.

#### Normal profiles

```
============================================================
Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}
------------------------------------------------------------
1. Sunrise City by Neon Echo [pop/happy] - Score: 7.66 (9.6/10)
   Because: matches your favorite genre (pop), fits the happy mood you like, energy level is close to what you want, has the produced/electronic sound you prefer
2. Gym Hero by Max Pulse [pop/intense] - Score: 7.59 (9.5/10)
   Because: matches your favorite genre (pop), has a feel similar to the happy mood, energy level is close to what you want, has the produced/electronic sound you prefer
3. Rooftop Lights by Indigo Parade [indie pop/happy] - Score: 7.31 (9.1/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop, fits the happy mood you like, energy level is close to what you want, has the produced/electronic sound you prefer
4. Concrete Sunrise by Verse Vandal [hip hop/energetic] - Score: 6.68 (8.3/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop, has a feel similar to the happy mood, energy level is close to what you want, has the produced/electronic sound you prefer
5. Basement Pulse by Nullwave [EDM/dark] - Score: 6.40 (8.0/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop, has a feel similar to the happy mood, energy level is close to what you want, has the produced/electronic sound you prefer
```

```
============================================================
Profile: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
------------------------------------------------------------
1. Library Rain by Paper Lanterns [lofi/chill] - Score: 7.86 (9.8/10)
   Because: matches your favorite genre (lofi), fits the chill mood you like, energy level is close to what you want, has the acoustic sound you prefer
2. Midnight Coding by LoRoom [lofi/chill] - Score: 7.57 (9.5/10)
   Because: matches your favorite genre (lofi), fits the chill mood you like, energy level is close to what you want, has the acoustic sound you prefer
3. Focus Flow by LoRoom [lofi/focused] - Score: 7.46 (9.3/10)
   Because: matches your favorite genre (lofi), has a feel similar to the chill mood, energy level is close to what you want, has the acoustic sound you prefer
4. Paper Boats by The Willowren [folk/dreamy] - Score: 7.09 (8.9/10)
   Because: has a similar audio profile (tempo, valence, danceability) to lofi, has a feel similar to the chill mood, energy level is close to what you want, has the acoustic sound you prefer
5. Spacewalk Thoughts by Orbit Bloom [ambient/chill] - Score: 7.01 (8.8/10)
   Because: has a similar audio profile (tempo, valence, danceability) to lofi, fits the chill mood you like, energy level is close to what you want, has the acoustic sound you prefer
```

```
============================================================
Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
------------------------------------------------------------
1. Storm Runner by Voltline [rock/intense] - Score: 7.88 (9.9/10)
   Because: matches your favorite genre (rock), fits the intense mood you like, energy level is close to what you want, has the amplified, heavy sound you prefer
2. Gym Hero by Max Pulse [pop/intense] - Score: 6.66 (8.3/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, fits the intense mood you like, energy level is close to what you want, has the produced/electronic sound you prefer
3. Basement Pulse by Nullwave [EDM/dark] - Score: 6.46 (8.1/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, has a feel similar to the intense mood, energy level is close to what you want, has the produced/electronic sound you prefer
4. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 6.04 (7.5/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, has a feel similar to the intense mood, energy level is close to what you want, has the produced/electronic sound you prefer
5. Iron Verdict by Ashfall [metal/aggressive] - Score: 5.77 (7.2/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, energy level is close to what you want, has the amplified, heavy sound you prefer
```

#### Adversarial / edge-case profiles

```
============================================================
Profile: Contradictory: high energy + sad
Preferences: {'genre': 'rock', 'mood': 'sad', 'energy': 0.95, 'likes_acoustic': False}
------------------------------------------------------------
1. Storm Runner by Voltline [rock/intense] - Score: 6.31 (7.9/10)
   Because: matches your favorite genre (rock), energy level is close to what you want, has the amplified, heavy sound you prefer
2. Iron Verdict by Ashfall [metal/aggressive] - Score: 5.59 (7.0/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, energy level is close to what you want, has the amplified, heavy sound you prefer
3. Basement Pulse by Nullwave [EDM/dark] - Score: 5.49 (6.9/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, energy level is close to what you want, has the produced/electronic sound you prefer
4. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 5.23 (6.5/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, energy level is close to what you want, has the produced/electronic sound you prefer
5. Gym Hero by Max Pulse [pop/intense] - Score: 4.98 (6.2/10)
   Because: has a similar audio profile (tempo, valence, danceability) to rock, energy level is close to what you want, has the produced/electronic sound you prefer
```

Note: `sad` now resolves to the catalog's `melancholic` centroid, so heavier
low-valence tracks (Iron Verdict) rise while the happy-sounding Gym Hero
(valence 0.77) is pushed to the bottom of the list. Storm Runner stays #1 —
intense rock is a defensible read of "high energy + sad."

```
============================================================
Profile: Contradictory: loud EDM + acoustic lover
Preferences: {'genre': 'EDM', 'mood': 'dark', 'energy': 0.95, 'likes_acoustic': True}
------------------------------------------------------------
1. Basement Pulse by Nullwave [EDM/dark] - Score: 6.92 (8.7/10)
   Because: matches your favorite genre (EDM), fits the dark mood you like, energy level is close to what you want — note: this isn't an acoustic track, unlike your stated preference
2. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 5.64 (7.1/10)
   Because: has a similar audio profile (tempo, valence, danceability) to EDM, has a feel similar to the dark mood, energy level is close to what you want — note: this isn't an acoustic track, unlike your stated preference
3. Gym Hero by Max Pulse [pop/intense] - Score: 5.55 (6.9/10)
   Because: has a similar audio profile (tempo, valence, danceability) to EDM, has a feel similar to the dark mood, energy level is close to what you want — note: this isn't an acoustic track, unlike your stated preference
4. Storm Runner by Voltline [rock/intense] - Score: 5.51 (6.9/10)
   Because: has a similar audio profile (tempo, valence, danceability) to EDM, has a feel similar to the dark mood, energy level is close to what you want — note: this isn't an acoustic track, unlike your stated preference
5. Rooftop Lights by Indigo Parade [indie pop/happy] - Score: 5.51 (6.9/10)
   Because: has a similar audio profile (tempo, valence, danceability) to EDM, has a feel similar to the dark mood, energy level is close to what you want — note: this isn't an acoustic track, unlike your stated preference
```

Note: the mutually exclusive "loud EDM + acoustic" request is now disclosed on
every result instead of silently ignored.

```
============================================================
Profile: Synonym resolution: k-pop / euphoric
Preferences: {'genre': 'k-pop', 'mood': 'euphoric', 'energy': 0.5, 'likes_acoustic': False}
------------------------------------------------------------
1. Sunrise City by Neon Echo [pop/happy] - Score: 6.81 (8.5/10)
   Because: matches your favorite genre (pop (interpreted from "k-pop")), has a feel similar to the uplifting (interpreted from "euphoric") mood, has the produced/electronic sound you prefer
2. Island Frequency by Coral Roots [reggae/uplifting] - Score: 6.61 (8.3/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop (interpreted from "k-pop"), fits the uplifting (interpreted from "euphoric") mood you like, energy level is close to what you want, has the clean, produced sound you prefer
3. Rooftop Lights by Indigo Parade [indie pop/happy] - Score: 6.57 (8.2/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop (interpreted from "k-pop"), has a feel similar to the uplifting (interpreted from "euphoric") mood, has the produced/electronic sound you prefer
4. Gym Hero by Max Pulse [pop/intense] - Score: 6.39 (8.0/10)
   Because: matches your favorite genre (pop (interpreted from "k-pop")), has a feel similar to the uplifting (interpreted from "euphoric") mood, has the produced/electronic sound you prefer
5. Concrete Sunrise by Verse Vandal [hip hop/energetic] - Score: 6.17 (7.7/10)
   Because: has a similar audio profile (tempo, valence, danceability) to pop (interpreted from "k-pop"), has a feel similar to the uplifting (interpreted from "euphoric") mood, has the produced/electronic sound you prefer
```

Note: `k-pop`→pop and `euphoric`→uplifting now resolve to real centroids. This
profile used to collapse to an identical flat-2.50 top 5 with the sparse and
neutral profiles; it now produces genuinely pop/uplifting results and states
how it interpreted the request.

```
============================================================
Profile: Truly unknown genre & mood
Preferences: {'genre': 'polka', 'mood': 'chaotic', 'energy': 0.5, 'likes_acoustic': False}
------------------------------------------------------------
1. Velvet Hours by Mila Sage [R&B/romantic] - Score: 2.50 (8.3/10)
   Because: energy level is close to what you want, has the produced/electronic sound you prefer — note: the catalog has nothing tagged "polka", so genre could not be matched; the catalog has no "chaotic" mood, so mood could not be matched
2. Island Frequency by Coral Roots [reggae/uplifting] - Score: 2.42 (8.1/10)
   Because: energy level is close to what you want, has the clean, produced sound you prefer — note: the catalog has nothing tagged "polka", so genre could not be matched; the catalog has no "chaotic" mood, so mood could not be matched
3. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 2.28 (7.6/10)
   Because: has the produced/electronic sound you prefer — note: the catalog has nothing tagged "polka", so genre could not be matched; the catalog has no "chaotic" mood, so mood could not be matched
4. Dusty Backroads by Hollis Grange [country/nostalgic] - Score: 2.28 (7.6/10)
   Because: energy level is close to what you want — note: the catalog has nothing tagged "polka", so genre could not be matched; the catalog has no "chaotic" mood, so mood could not be matched; this is more acoustic/organic than you usually pick
5. Concrete Sunrise by Verse Vandal [hip hop/energetic] - Score: 2.22 (7.4/10)
   Because: has the produced/electronic sound you prefer — note: the catalog has nothing tagged "polka", so genre could not be matched; the catalog has no "chaotic" mood, so mood could not be matched
```

Note: genuinely unknown labels (no exact match, no synonym) still cannot score,
but the raw score is honestly low **and** the `/10` excludes the unmatchable
genre/mood terms — so an audio-only match reads 8.3/10 instead of looking
broken, and the "note:" says exactly why genre and mood were dropped.

```
============================================================
Profile: Sparse: energy only
Preferences: {'energy': 0.5}
------------------------------------------------------------
1. Velvet Hours by Mila Sage [R&B/romantic] - Score: 2.50 (8.3/10)
   Because: energy level is close to what you want, has the produced/electronic sound you prefer
2. Island Frequency by Coral Roots [reggae/uplifting] - Score: 2.42 (8.1/10)
   Because: energy level is close to what you want, has the clean, produced sound you prefer
3. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 2.28 (7.6/10)
   Because: has the produced/electronic sound you prefer
4. Dusty Backroads by Hollis Grange [country/nostalgic] - Score: 2.28 (7.6/10)
   Because: energy level is close to what you want — note: this is more acoustic/organic than you usually pick
5. Concrete Sunrise by Verse Vandal [hip hop/energetic] - Score: 2.22 (7.4/10)
   Because: has the produced/electronic sound you prefer
```

```
============================================================
Profile: Neutral / boundary
Preferences: {'genre': '', 'mood': '', 'energy': 0.5, 'likes_acoustic': False}
------------------------------------------------------------
1. Velvet Hours by Mila Sage [R&B/romantic] - Score: 2.50 (8.3/10)
   Because: energy level is close to what you want, has the produced/electronic sound you prefer
2. Island Frequency by Coral Roots [reggae/uplifting] - Score: 2.42 (8.1/10)
   Because: energy level is close to what you want, has the clean, produced sound you prefer
3. Night Drive Loop by Neon Echo [synthwave/moody] - Score: 2.28 (7.6/10)
   Because: has the produced/electronic sound you prefer
4. Dusty Backroads by Hollis Grange [country/nostalgic] - Score: 2.28 (7.6/10)
   Because: energy level is close to what you want — note: this is more acoustic/organic than you usually pick
5. Concrete Sunrise by Verse Vandal [hip hop/energetic] - Score: 2.22 (7.4/10)
   Because: has the produced/electronic sound you prefer
```

### What the adversarial testing found (and what changed)

The adversarial profiles originally exposed three real defects; all three were
addressed, and the edge-case profiles are kept as regression checks:

- **Unknown labels are no longer silently dropped.** Recognized synonyms
  (`sad`→melancholic, `k-pop`→pop, `euphoric`→uplifting) now resolve onto the
  catalog's existing data-derived centroids, so a request the catalog has never
  literally seen still scores against real music instead of collapsing to a
  flat low score shared by every vague query. Truly unknown labels (`polka`,
  `chaotic`) still cannot match — but the explanation now says so explicitly.
- **Impossible preferences are disclosed, not hidden.** When a stated
  preference cannot be honored (e.g. an acoustic lover asking for loud EDM), the
  explanation appends an honest "note:" rather than quietly omitting the reason.
- **Low-information queries read sensibly.** The displayed `/10` score excludes
  genre/mood terms that cannot be matched, so a song matched purely on audio
  features scores a high fraction of what was *achievable* instead of looking
  broken next to a fully-specified profile. Raw scores are unchanged, so
  ranking is unaffected.
- **Remaining limitation.** With only one `rock` and one `melancholic` song in
  the catalog, those "centroids" are effectively single points, so genre/mood
  similarity is noisy for sparse labels. More catalog coverage would sharpen it.

---

## 8. Future Work  

**Ideas for improvement.**

1. **More songs.** A bigger catalog would fix the "one song per tag" problem
   and make near-match scores much better.
2. **More variety in the top 5.** Right now similar songs can bunch up. We
   could push for a mix of genres or moods in the list.
3. **Smarter mood handling.** Map moods to feel numbers (like valence) so
   "sad" or "angry" work even without a matching label.

---

## 9. Personal Reflection  

**Biggest learning moment.** I learned that a recommender is mostly a set of
scoring rules. Small choices, like how much genre is worth, change the whole
list. The turning point was the adversarial testing. When I fed the system
conflicting wishes (high energy + sad), I saw it quietly drop the part it could
not handle. That taught me the real work is not the math. It is deciding how
the system should act when the request does not fit the data.

**How AI tools helped, and when I checked them.** The AI assistant helped me
move fast. It drafted the scoring code, suggested tricky test profiles, and
explained trade-offs between ideas. But I did not take it on trust. I asked it
to show the exact points behind each top pick, and I checked that math against
the CSV by hand. I also pushed back on a few of its suggestions. For example, I
did not want a hard-coded "genre family" table, so we fixed the wording of the
reasons instead. The rule I followed: let AI draft and explain, but verify the
numbers and own the design choices myself.

**What surprised me.** A simple weighted sum still "feels" like a
recommendation. There is no learning and no fancy model, just add up a few
points and sort. Yet the reasons it prints make it feel smart. That showed me
how much of the "magic" in real apps might be plain rules plus a good
explanation.

**What I would try next.** I would grow the catalog so each tag has more than
one song, since that is the biggest weakness. I would add variety to the top 5
so similar tracks do not bunch up. And I would map moods to feel numbers (like
valence) so words like "sad" or "angry" work even without an exact label.
