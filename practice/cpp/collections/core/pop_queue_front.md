# Name

Pop Queue Front

# Description

For a mutable `std::queue<int>`, return and remove the oldest integer as `std::optional<int>`, or return an empty optional if the queue is empty. This exercise covers safely reading before removing from a queue.

# Solution

```cpp
if (values.empty()) {
    return std::nullopt;
}
int result = values.front();
values.pop();
return result;
```
