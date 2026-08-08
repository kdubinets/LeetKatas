# Name

Specialize Hash for a Value Type

# Description

Provide the permitted `std::hash` specialization for the user-defined `UserId` value type so it can use the default unordered-container hashing policy. Hash exactly the integer field used by its equality operator.

# Solution

```cpp
template<>
struct std::hash<UserId> {
    std::size_t operator()(UserId id) const noexcept {
        return std::hash<int>{}(id.value);
    }
};
```
