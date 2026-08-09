# Name

Query an Input's End Position

# Description

Clear any prior state on a seekable caller-provided `std::istream&`, move to the end, and return that end position. Return an empty optional if seeking or position reporting fails. The stream may remain positioned at the end, and the returned opaque `std::streampos` is not presented as a portable byte count. This exercise covers end-relative seeking and querying an input position.

# Solution

```cpp
input.clear();
input.seekg(0, std::ios::end);
if (!input) {
    return std::nullopt;
}
auto position = input.tellg();
if (position == std::streampos{-1}) {
    return std::nullopt;
}
return position;
```
