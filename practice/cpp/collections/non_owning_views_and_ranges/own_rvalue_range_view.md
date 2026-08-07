# Name

Own an Rvalue Range View

# Description

Given a string vector by value, transfer it into a range view that owns the vector and therefore keeps all element storage alive after the function returns. This exercise covers lifetime-safe adaptation of an rvalue range rather than returning a dangling reference view.

# Solution

```cpp
return std::views::all(std::move(values));
```
