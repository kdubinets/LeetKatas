# Name

View a Vector Tail

# Description

Given a const string vector and a valid start index no greater than its size, return a read-only span over the suffix beginning there. The vector remains the owner and no strings are copied. This exercise covers safely returning a non-owning view into caller-owned storage.

# Solution

```cpp
return std::span{values}.subspan(start);
```
