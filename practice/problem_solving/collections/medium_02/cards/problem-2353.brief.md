# Design a Food Rating System

Build a system from parallel arrays of distinct food names, each food's
cuisine, and its initial integer rating. It must support:

- `changeRating(food, newRating)`: replace that food's current rating.
- `highestRated(cuisine)`: return the name of the highest-rated food of that
  cuisine, choosing the lexicographically smaller name on a rating tie.

Lexicographic order is dictionary order; if one name is a prefix of another,
the shorter name comes first.

A food's cuisine never changes. Queries name existing foods or cuisines, and
every queried cuisine has at least one food. There are at most `2 × 10^4`
foods and at most `2 × 10^4` operations. Names use lowercase English letters
and have at most 10 characters; ratings are between 1 and `10^8`.
