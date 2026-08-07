# Name

Make a Bounded Iota View

# Description

Return a lazy finite range of integers beginning at `first` and ending before `last`, where `first <= last`. Do not allocate a container. This exercise covers constructing an iterator-and-sentinel iota view with explicit bounds.

# Solution

```cpp
return std::views::iota(first, last);
```
