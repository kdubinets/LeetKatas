# Name

Advance to Next Permutation

# Description

Mutate an integer vector to its next lexicographical permutation and return whether such a greater arrangement existed. If the input was the greatest permutation, rearrange it to the smallest and return false. This exercise covers permutation advancement and its result object.

# Solution

```cpp
return std::ranges::next_permutation(values).found;
```
