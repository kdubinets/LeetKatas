# Name

Patch an Output Position

# Description

For a seekable caller-provided `std::ostream&`, clear any prior state, move the write position to the supplied valid absolute `std::streampos`, and replace the character there with `value`. Return whether positioning and output both succeed. This exercise covers output positioning and single-character unformatted output without taking ownership of the stream.

# Solution

```cpp
output.clear();
output.seekp(position);
if (!output) {
    return false;
}
output.put(value);
return static_cast<bool>(output);
```
