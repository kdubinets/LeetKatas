# Name

Rewind an Input Stream

# Description

Restore a possibly exhausted seekable `std::istream&` and reposition it at the beginning. Return whether the stream is successful after the operation. This exercise covers the required state reset before seeking a stream that may hold EOF or failure flags.

# Solution

```cpp
input.clear();
input.seekg(0, std::ios::beg);
return static_cast<bool>(input);
```
