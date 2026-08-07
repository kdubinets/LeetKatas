# Name

Return a Local by Implicit Move

# Description

Return a by-value local string so the language can elide the construction or move automatically. Do not force an explicit move, which can inhibit elision. This exercise covers implicit move treatment of eligible local return expressions.

# Solution

```cpp
return value;
```
