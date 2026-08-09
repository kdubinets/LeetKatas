# Name

Mark an Unlikely Empty Branch

# Description

Handle empty text with an early zero return and apply the C++20 likelihood attribute to that branch's statement. Return the view's size for nonempty input without changing the text.

# Solution

```cpp
if (text.empty()) [[unlikely]] {
    return 0;
}
return text.size();
```
