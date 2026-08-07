# Name

Move a String into an Optional

# Description

Replace a mutable optional string with the value of a mutable source string by moving it. The source must remain valid but may have unspecified contents afterward. This exercise covers moving a value into optional storage.

# Solution

```cpp
destination = std::move(source);
```
