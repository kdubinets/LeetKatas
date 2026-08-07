# Name

Store a Unique Owner

# Description

Append a by-value `std::unique_ptr<Task>` to a vector of exclusive owners, transferring rather than copying ownership. This exercise covers storing a move-only owner in a standard container.

# Solution

```cpp
tasks.push_back(std::move(task));
```
