# Name

Hash Case-Insensitive Text Consistently

# Description

Implement a hash for text whose supplied equality policy ignores ASCII letter case. Fold each character before incorporating it so any two values considered equal are guaranteed to have the same hash.

# Solution

```cpp
std::size_t result = 0;
for (char ch : text) {
    result = result * 131U + static_cast<unsigned char>(ascii_lower(ch));
}
return result;
```
