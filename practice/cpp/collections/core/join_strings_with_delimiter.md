# Name

Join Strings with Delimiter

# Description

Join a const vector of strings into one string with exactly one supplied delimiter between adjacent elements and none at either end. An empty input produces an empty string. This exercise covers delimiter-aware string accumulation without special output cleanup.

# Solution

```cpp
for (std::size_t index = 0; index < values.size(); ++index) {
    if (index != 0) {
        result += delimiter;
    }
    result += values[index];
}
```
