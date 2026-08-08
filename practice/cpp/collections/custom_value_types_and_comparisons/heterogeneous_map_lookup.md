# Name

Look Up a Map Key Heterogeneously

# Description

Read a price from a const map with custom `Ticket` keys using a plain integer number. Use the supplied transparent comparator and return no value when absent without constructing a `Ticket`.

# Solution

```cpp
const auto it = prices.find(number);
if (it == prices.end()) {
    return std::nullopt;
}
return it->second;
```
