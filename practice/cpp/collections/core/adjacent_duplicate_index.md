# Name

Adjacent Duplicate Index

# Description

Find the first adjacent equal pair in a const integer vector and return the index of the pair's first element as `std::optional<std::size_t>`. Return an empty optional if no adjacent duplicate exists. This exercise covers adjacent-pair search and iterator-to-index conversion.

# Solution

```cpp
auto it = std::ranges::adjacent_find(values);
return it == values.end()
           ? std::nullopt
           : std::optional<std::size_t>{
                 static_cast<std::size_t>(it - values.begin())};
```
