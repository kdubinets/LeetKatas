# Name

Require an Exact Result Type

# Description

Define `ExactSize<T>` with a compound requirement. Calling `.size()` on a const `T` must be valid and its expression type must be exactly `std::size_t`.

# Solution

```cpp
concept ExactSize = requires(const T& value) {
    { value.size() } -> std::same_as<std::size_t>;
};
```
