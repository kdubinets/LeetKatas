# Name

Deduce an Array Bound

# Description

Define `array_length` so a built-in array's element type and bound are deduced from a const array reference. Return the bound as `std::size_t` without accepting pointers.

# Solution

```cpp
template <class T, std::size_t Size>
constexpr std::size_t array_length(const T (&)[Size]) {
    return Size;
}
```
