# Twisted Mirror Path Count

A robot starts at the top-left empty cell of a binary grid and aims to reach
the bottom-right empty cell. From an empty cell, it may attempt to move right
or down. A `1` cell is a mirror that redirects the attempted move **before**
the robot enters it: approaching from the left skips directly to the cell
below the mirror; approaching from above skips directly to the cell to its
right. The robot does not choose a direction at a mirror. If the next cell is
also a mirror, reflect again according to the direction of arrival. A path
that leaves the grid is invalid.

Count the distinct valid paths to the destination, modulo `10^9 + 7`.
The grid dimensions are each between 2 and 500, and both endpoint cells are
`0`. For example, an all-zero `2 × 2` grid has two valid paths.
For `[[0,1,1],[1,1,0]]`, exactly one path reaches the destination; the
other first-step choice reflects out of bounds.
