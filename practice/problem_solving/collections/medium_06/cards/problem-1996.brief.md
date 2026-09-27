# The Number of Weak Characters in the Game

Each character has an attack and defense value, given as `properties[i]=[attack,defense]`. A character is weak if **another** character has both strictly greater attack and strictly greater defense. Count weak characters.

`2 <= |properties| <= 100000`; both values lie in `[1,100000]`. Equal attack or equal defense does not satisfy the strict comparison.
