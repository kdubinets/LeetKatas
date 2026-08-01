# Name

Generate Arithmetic Progression

# Description

Return an integer vector of the requested size whose values begin at `first` and repeatedly increase by `step`. All generated values are guaranteed representable as `int`. This exercise covers range generation with initialized, mutable lambda state.

# Solution

```cpp
std::ranges::generate(result, [value = first, step, remaining = count]() mutable {
    int current = value;
    if (--remaining != 0) {
        value += step;
    }
    return current;
});
```
