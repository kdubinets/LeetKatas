# Name

Require a Convertible Result Type

# Description

Define `StringNamed<T>` with a compound requirement. Calling `.name()` on a const `T` must be valid, and the expression result must be implicitly convertible to `std::string_view` without requiring that exact result type.

# Solution

```cpp
concept StringNamed = requires(const T& value) {
    { value.name() } -> std::convertible_to<std::string_view>;
};
```
