# Stone Game VII

Two players alternate removing either end stone from a row of positive-valued stones. The player who removes a stone scores the sum of the stones **remaining after that removal**. Alice moves first and tries to maximize her final score minus Bob’s; Bob tries to minimize that difference. Return the difference under optimal play.

There are `2` to `1,000` stones, each worth `1` to `1,000`. Removing the last stone scores zero.
