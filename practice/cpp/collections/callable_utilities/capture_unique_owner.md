# Name

Capture a Unique Owner

# Description

Transfer a non-null `std::unique_ptr<int>` into a returned lambda. The callable must own the allocation after `solve` returns and produce the stored integer when called; it is intentionally move-only.

# Solution

```cpp
return [owned = std::move(value)] { return *owned; };
```
