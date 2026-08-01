# Name

Find Set Value Position

# Description

Find an integer in a const ordered set and return its zero-based `std::size_t` position in ascending iteration order, or an empty optional when absent. This exercise covers measuring distance between non-random-access iterators.

# Solution

```cpp
auto it = values.find(target);
return it == values.end()
           ? std::nullopt
           : std::optional<std::size_t>{
                 static_cast<std::size_t>(std::distance(values.begin(), it))};
```
