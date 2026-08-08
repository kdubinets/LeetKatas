# Name

Clear a Stored Callback

# Description

Reset a mutable `std::function<void()>` so it no longer contains a callable target. Any resources owned by the previous target should be released through normal assignment semantics.

# Solution

```cpp
callback = nullptr;
```
