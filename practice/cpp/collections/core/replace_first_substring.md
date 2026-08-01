# Name

Replace First Substring

# Description

Replace the first occurrence of a guaranteed nonempty target string inside a mutable string and return whether a replacement occurred. Leave the text unchanged if the target is absent. This exercise covers combining substring search with bounded replacement.

# Solution

```cpp
auto position = text.find(target);
if (position == std::string::npos) {
    return false;
}
text.replace(position, target.size(), replacement);
return true;
```
