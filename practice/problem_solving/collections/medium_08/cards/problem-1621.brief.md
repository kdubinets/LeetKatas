# Number of Sets of K Non-Overlapping Line Segments

The n available points lie at coordinates `0,1,...,n-1` on a line. Count sets of exactly k segments whose endpoints are these points. Each segment must have distinct endpoints and cover at least two available points. Segment interiors may not overlap, but segments may share an endpoint. Points need not all be covered. Return the count modulo `1000000007`.

`2 <= n <= 1000`; `1 <= k <= n-1`. A set is counted once regardless of the order in which its segments are listed.
