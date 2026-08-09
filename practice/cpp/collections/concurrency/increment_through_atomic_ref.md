# Name

Increment Through an Atomic Reference

# Description

Apply one atomic increment to caller-owned, suitably aligned ordinary integer storage without changing its declared type. All concurrent accesses during the atomic view's lifetime are required to be atomic. This exercise covers C++20 `std::atomic_ref`.

# Solution

```cpp
std::atomic_ref reference(value);
reference.fetch_add(1);
```
