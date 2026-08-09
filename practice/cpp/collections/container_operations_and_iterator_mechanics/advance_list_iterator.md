# Name

Advance a List Iterator

# Description

Move a mutable `std::list<int>::iterator` forward by `steps` and return the resulting position. The supplied distance is representable by the iterator's difference type and does not advance past the end. This exercise covers distance-based mutation of a non-random-access iterator.

# Solution

```cpp
using difference_type = std::iterator_traits<Iterator>::difference_type;
std::advance(position, static_cast<difference_type>(steps));
return position;
```
