# Maximize the Profit as the Salesman

Houses lie on a line at indices `0` through `n-1`. Each offer `[start,end,gold]` proposes buying **all** houses in that inclusive interval for the stated gold. Choose any offers to maximize total gold, with no house sold to two buyers; houses may remain unsold. Return the maximum. There are at most 100,000 houses and 100,000 offers; gold per offer is 1–1,000.

Offers `[0,0,1]`, `[0,2,2]`, and `[1,3,2]` on five houses permit profit 3 by taking the first and third.
