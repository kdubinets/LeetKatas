# Name

Consume Leading Digits from a View

# Description

Return the maximal leading sequence of ASCII digits from a mutable `std::string_view`, then advance the input view beyond those digits. An input beginning with a nondigit produces an empty result without advancing, and an all-digit input is consumed completely. This exercise covers allocation-free predicate-defined token consumption.

# Solution

```cpp
auto length = remaining.find_first_not_of("0123456789");
auto digits = remaining.substr(0, length);
remaining.remove_prefix(digits.size());
return digits;
```
