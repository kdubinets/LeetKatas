# Name

Order Points with Deterministic Ties

# Description

Define a strict ordering for points using squared distance from the origin, followed by x and y coordinates to break ties. Coordinates are small enough that the squared arithmetic fits `long long`.

# Solution

```cpp
const auto key = [](Point point) {
    const auto x = static_cast<long long>(point.x);
    const auto y = static_cast<long long>(point.y);
    return std::tuple{x * x + y * y, point.x, point.y};
};
return key(left) < key(right);
```
