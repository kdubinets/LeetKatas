# Name

Select an Iterator Subrange

# Description

Given valid half-open indices `first <= last <= values.size()`, return a borrowed `std::ranges::subrange` over those elements of a const vector. The vector retains ownership and no elements are copied. This exercise covers packaging an iterator pair as a range.

# Solution

```cpp
using difference_type = std::vector<int>::difference_type;
return {values.begin() + static_cast<difference_type>(first),
        values.begin() + static_cast<difference_type>(last)};
```
