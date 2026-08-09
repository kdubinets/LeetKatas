# Name

Seek an Input Position

# Description

For a seekable caller-provided `std::istream&`, clear any prior state, move the read position to the supplied valid absolute `std::streampos`, and return the resulting position. Return an empty optional if seeking or position reporting fails. This exercise covers restoring an opaque stream position after a stream may have reached EOF.

# Solution

```cpp
input.clear();
input.seekg(position);
if (!input) {
    return std::nullopt;
}
auto resulting_position = input.tellg();
if (resulting_position == std::streampos{-1}) {
    return std::nullopt;
}
return resulting_position;
```
