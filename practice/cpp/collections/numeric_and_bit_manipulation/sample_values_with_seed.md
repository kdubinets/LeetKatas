# Name

Sample Values with a Seed

# Description

Return a pseudorandom sample of `count` elements from a const vector without replacement or input mutation. The count does not exceed the input size, and a supplied 32-bit seed initializes a local standard Mersenne Twister engine. This exercise covers `std::sample` with dynamic output and deterministic engine construction.

# Solution

```cpp
std::mt19937 engine{seed};
std::vector<int> result;
result.reserve(count);
std::sample(values.begin(), values.end(), std::back_inserter(result), count, engine);
return result;
```
