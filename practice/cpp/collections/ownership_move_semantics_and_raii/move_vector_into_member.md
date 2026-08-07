# Name

Move a Vector into a Member

# Description

Replace a `Batch` object's vector with the contents of a distinct mutable source vector by move assignment. The source remains valid with unspecified contents, and the destination's old elements are cleaned up. This exercise covers transferring container-owned allocation into object storage.

# Solution

```cpp
destination.values = std::move(source);
```
