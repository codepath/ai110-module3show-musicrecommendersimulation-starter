# Reflection: Comparing User Profile Outputs

## Jackie (lofi/chill) vs Alex (pop/happy)

These two profiles are almost opposites in energy and genre, and the results showed that clearly. Jackie got quiet, low-energy lofi tracks at the top, while Alex got upbeat pop songs. The interesting part is *why* — it's not just that they prefer different genres, it's that the energy levels are far apart (0.4 vs 0.8), so even if the same song showed up in both lists, it would score much lower for one of them. This shows the energy feature is doing real work, not just acting as a tiebreaker.

## Alex (pop/happy) vs Sam (rock/intense)

Both are high-energy profiles, which is why *Gym Hero* kept appearing in both lists. It's a pop song with intense mood and 0.93 energy — close enough on energy to rank well for Sam even though the genre doesn't match. This is a good example of why *Gym Hero* shows up for people who "just want happy pop" — it has a matching energy level, and since energy contributes 0.25 to the score, a near-perfect energy match is worth more than you might expect. If genre were weighted higher, *Gym Hero* would stop appearing in Sam's results entirely.

## Jordan (conflicting: high-energy + sad) vs Jackie (lofi/chill)

Jordan and Jackie are a useful contrast. Jackie's results made intuitive sense — chill songs for a chill listener. Jordan's top pick (*Rainy Window*) was correct, but the rest of the list was full of intense songs that matched on energy alone. The difference is that Jackie's preferences don't conflict — low energy and chill mood go together naturally. Jordan's don't — high energy and sad mood are unusual together, and the catalog has almost nothing that fits both. The system can't tell the difference between a "coherent" profile and a conflicting one; it just adds up the numbers.

## Riley (reggae/no catalog match) vs Payton (indie pop/moody)

Payton got a nearly perfect 0.98 match because *Late Night Overthinking* happened to align on all three features. Riley, with no reggae in the catalog, maxed out at 0.72 — and even that felt like a stretch. The difference isn't about the quality of their preferences, it's purely about catalog coverage. This is a bias worth naming: the system works better for users whose taste happens to be represented in the data. Riley didn't do anything wrong — the data just wasn't built with them in mind.
