# Name

Detect a Size Member

# Description

Partially specialize `has_size_member` when calling `.size()` on a const `T` expression is well-formed. Use the primary template's second parameter as the detection slot.

# Solution

```cpp
template <class T>
struct has_size_member<T, std::void_t<decltype(std::declval<const T&>().size())>>
    : std::true_type {};
```
