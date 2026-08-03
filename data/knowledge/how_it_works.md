# How MoodMatch Works

Reference answers about how the recommender itself behaves. The chat assistant
retrieves from this document when a user asks *how* recommendations are made or
*what* the system can do, instead of asking for songs.

## How are recommendations scored?
MoodMatch is a content-based recommender. It scores every song as a weighted sum
of four things: genre (weight 3.0), mood (weight 2.0), energy closeness (weight
2.0), and acoustic fit (weight 1.0). An exact genre or mood match earns full
weight; a non-exact match earns partial credit based on how similar the song's
audio profile (tempo, valence, danceability) is to that genre's or mood's average.
The songs are ranked by total score and the top matches are returned.

## Why does each pick come with a reason?
Being explainable is a core goal. Every scoring term records a short reason, so
each recommendation lists why it was chosen — and honestly notes when a stated
preference could not be met.

## What is a synonym / out-of-vocabulary term?
If you ask for a genre or mood the catalog does not literally contain, a synonym
table maps it onto the closest known label. For example "k-pop" maps to "pop" and
"sad" maps to "melancholic", so your request still scores against real data. Truly
unknown words like "polka" stay unmatched and are reported honestly.

## What is energy?
Energy is a 0.0 to 1.0 measure of a song's intensity. High-energy cues in a
request (workout, pumped, intense) target around 0.9; low-energy cues (chill,
study, calm) target around 0.3.

## What is acousticness?
Acousticness is a 0.0 to 1.0 measure of how acoustic (organic) versus produced
(electronic) a song sounds. High acousticness means acoustic instruments; low
means produced or electronic.

## How big is the catalog?
The catalog is small and fixed: 18 songs. MoodMatch is a teaching-scale system,
not a production service, so it cannot recommend anything outside those 18 songs.

## Does MoodMatch use my listening history?
No. It has no crowd data and no history. It only matches the taste you state in
your request to the measurable attributes of each song.
