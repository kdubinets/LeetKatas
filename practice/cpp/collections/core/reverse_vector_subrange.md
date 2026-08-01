# Name

Reverse Vector Subrange

# Description

Reverse in place the valid half-open interval `[first, last)` of a mutable integer vector, where both bounds are `std::size_t` indices satisfying `first <= last <= values.size()`. Values outside the interval must retain their positions. This exercise covers converting validated indices into a range operation.

# Solution

```cpp
using difference_type = std::vector<int>::difference_type;
std::ranges::reverse(
    values.begin() + static_cast<difference_type>(first),
    values.begin() + static_cast<difference_type>(last));
```
