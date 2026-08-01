# Name

Uppercase ASCII String

# Description

Mutate a `std::string` by converting every lowercase ASCII letter from `a` through `z` to its uppercase counterpart while leaving all other bytes unchanged. This exercise covers an in-place character transformation with a lambda.

# Solution

```cpp
std::ranges::transform(text, text.begin(), [](char character) {
    return character >= 'a' && character <= 'z'
               ? static_cast<char>(character - 'a' + 'A')
               : character;
});
```
