

1. High-Energy Pop vs Chill Lofi: The pop profile pushes upbeat produced tracks with higher energy, while Chill Lofi shifts to softer acoustic songs because lower target energy and acoustic preference both align with lofi entries.

2. High-Energy Pop vs Deep Intense Rock: Both profiles like high energy and produced sound, but genre and mood split them, so pop gets Sunrise City while rock gets Storm Runner.

3. High-Energy Pop vs High-Energy Sad (mood never exists): These two are almost the same profile except mood, so rankings stay similar, which shows genre and energy still dominate when mood has no matching songs.

4. High-Energy Pop vs Genre Ghost - Classical (genre absent): Pop gets clear top matches from genre alignment, while classical falls back to mood, energy, and acoustic clues because no classical songs exist.

5. High-Energy Pop vs Conflicted Acoustic Rocker: High-Energy Pop rewards produced sound, but Conflicted Acoustic Rocker loses points on top rock songs due to acoustic mismatch and starts pulling in softer acoustic tracks lower in the list.

6. High-Energy Pop vs Mid-Energy Ambiguous (energy=0.5): Both can return produced tracks, but the mid-energy profile gives weaker confidence because its target sits between clusters in the dataset.

7. High-Energy Pop vs Perfect Mismatch (no genre or mood in catalog): Pop has strong top scores from direct matches, while Perfect Mismatch mostly ranks songs by energy closeness and produced-sound preference.

8. Chill Lofi vs Deep Intense Rock: These profiles are almost opposites, so Chill Lofi gets low-energy acoustic songs and Deep Intense Rock gets high-energy non-acoustic tracks.

9. Chill Lofi vs High-Energy Sad (mood never exists): Chill Lofi can use mood plus acoustic alignment, while High-Energy Sad cannot use mood at all and leans toward energetic pop.

10. Chill Lofi vs Genre Ghost - Classical (genre absent): Both can land on Coffee Shop Stories and lofi-adjacent songs because acoustic and moderate energy are strong signals, but Chill Lofi has better ranking confidence from genre matches.

11. Chill Lofi vs Conflicted Acoustic Rocker: Both like acoustic texture, but Chill Lofi has matching low energy and mood, while Conflicted Acoustic Rocker conflicts with rock songs that are mostly non-acoustic.

12. Chill Lofi vs Mid-Energy Ambiguous (energy=0.5): Chill Lofi strongly favors low-energy chill songs, while mid-energy ambiguous keeps some produced tracks because it requests synthwave and moody mood.

13. Chill Lofi vs Perfect Mismatch (no genre or mood in catalog): Chill Lofi has clear semantic matches; Perfect Mismatch gets generic fallback recommendations because neither genre nor mood can match.

14. Deep Intense Rock vs High-Energy Sad (mood never exists): Both prefer high energy, but rock intensity gives Storm Runner a strong lead whereas High-Energy Sad drifts to pop tracks due to genre alignment.

15. Deep Intense Rock vs Genre Ghost - Classical (genre absent): Deep Intense Rock has at least one direct genre anchor, while Genre Ghost has no genre anchor and relies on weaker fallback cues.

16. Deep Intense Rock vs Conflicted Acoustic Rocker: These are similar except acoustic preference, and that one change lowers confidence for rock results because the best rock song is not acoustic.

17. Deep Intense Rock vs Mid-Energy Ambiguous (energy=0.5): Rock-intense targets a narrow high-energy zone; mid-energy ambiguous spreads to mixed tracks because its energy and genre combination is less concentrated.

18. Deep Intense Rock vs Perfect Mismatch (no genre or mood in catalog): Deep Intense Rock still finds an obvious top match, while Perfect Mismatch gets a flat list with smaller score gaps.

19. High-Energy Sad (mood never exists) vs Genre Ghost - Classical (genre absent): High-Energy Sad keeps genre support from pop, but Genre Ghost loses genre support and must rely mostly on relaxed mood and acoustic fit.

20. High-Energy Sad (mood never exists) vs Conflicted Acoustic Rocker: High-Energy Sad benefits from produced-sound matches in pop songs, while Conflicted Acoustic Rocker loses points when high-energy rock is non-acoustic.

21. High-Energy Sad (mood never exists) vs Mid-Energy Ambiguous (energy=0.5): Both are somewhat unstable, but High-Energy Sad still has genre anchors whereas mid-energy ambiguous depends more on partial similarity.

22. High-Energy Sad (mood never exists) vs Perfect Mismatch (no genre or mood in catalog): High-Energy Sad can still use genre and energy, but Perfect Mismatch has neither semantic anchor and becomes mostly an energy-based ranking.

23. Genre Ghost - Classical (genre absent) vs Conflicted Acoustic Rocker: Genre Ghost likes acoustic moderate-energy songs and avoids non-acoustic bias, while Conflicted Acoustic Rocker pulls in contradictory results because its genre and acoustic goals fight each other.

24. Genre Ghost - Classical (genre absent) vs Mid-Energy Ambiguous (energy=0.5): Both are edge cases, but Genre Ghost is constrained by missing genre whereas Mid-Energy Ambiguous still has a real synthwave/mood anchor.

25. Genre Ghost - Classical (genre absent) vs Perfect Mismatch (no genre or mood in catalog): Genre Ghost still gets some mood guidance (relaxed), while Perfect Mismatch has no genre or mood guidance and falls back almost entirely to numeric proximity.

26. Conflicted Acoustic Rocker vs Mid-Energy Ambiguous (energy=0.5): Conflicted Acoustic Rocker has stronger intent but contradictory constraints; Mid-Energy Ambiguous has weaker intent but fewer hard conflicts.

27. Conflicted Acoustic Rocker vs Perfect Mismatch (no genre or mood in catalog): Conflicted Acoustic Rocker can still hit rock and intense signals, while Perfect Mismatch has no direct semantic matches and therefore flatter, less meaningful rankings.

28. Mid-Energy Ambiguous (energy=0.5) vs Perfect Mismatch (no genre or mood in catalog): Mid-Energy Ambiguous still gets a strong top song from synthwave and moody alignment, but Perfect Mismatch cannot and mostly ranks by energy and production style.

Overall, these comparisons make sense with the scoring logic: direct genre and mood matches create confident top results, while missing or conflicting preferences force fallback behavior that feels less personalized.