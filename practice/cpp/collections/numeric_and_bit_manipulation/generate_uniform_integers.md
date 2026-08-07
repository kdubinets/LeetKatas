# Name

Generate Uniform Integers

# Description

Return `count` pseudorandom `int` values distributed uniformly over the inclusive interval from `low` through `high`. The bounds are ordered, and a supplied 32-bit seed initializes a local standard Mersenne Twister engine. This exercise covers pairing a random engine with a reusable uniform integer distribution.

# Solution

```cpp
std::mt19937 engine{seed};
std::uniform_int_distribution<int> distribution{low, high};
std::vector<int> values(count);
std::generate(values.begin(), values.end(), [&] { return distribution(engine); });
return values;
```
