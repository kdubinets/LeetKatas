# Name

Reuse a Moved-From String

# Description

Move a mutable source string into a distinct mutable destination, then assign `"ready"` to the moved-from source. Do not inspect or depend on the source's intermediate contents. This exercise covers safe reuse of a valid but unspecified moved-from standard-library object.

# Solution

```cpp
destination = std::move(source);
source = "ready";
```
