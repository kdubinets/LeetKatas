# Name

Declare a Move-Only Owner

# Description

Complete the special-member declarations for an `Owner` containing a unique pointer. It must support move construction and move assignment, forbid both copy operations, and need no handwritten transfer logic. This exercise covers explicitly expressing a move-only class interface.

# Solution

```cpp
Owner(const Owner&) = delete;
Owner& operator=(const Owner&) = delete;
Owner(Owner&&) noexcept = default;
Owner& operator=(Owner&&) noexcept = default;
```
