# Name

Partially Specialize a Pointer Trait

# Description

Partially specialize `is_raw_pointer` for types matching `T*` and derive that specialization from `std::true_type`. The primary template must remain false for non-pointers.

# Solution

```cpp
template <class T>
struct is_raw_pointer<T*> : std::true_type {};
```
