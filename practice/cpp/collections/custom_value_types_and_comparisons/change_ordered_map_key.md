# Name

Safely Change an Ordered Map Key

# Description

Replace an existing custom map key while preserving its mapped string without copying that string. Return false without changing the map when the old key is absent. The new key is guaranteed not to exist already.

# Solution

```cpp
auto node = values.extract(old_key);
if (node.empty()) {
    return false;
}
node.key() = std::move(new_key);
values.insert(std::move(node));
return true;
```
