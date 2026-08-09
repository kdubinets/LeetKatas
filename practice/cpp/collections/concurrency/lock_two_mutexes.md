# Name

Lock Two Mutexes Together

# Description

Acquire the two distinct supplied mutexes as one scoped operation, then exchange their protected integers. The implementation must not impose a hand-written lock order, so concurrent calls with reversed arguments cannot deadlock through inconsistent acquisition order.

# Solution

```cpp
std::scoped_lock lock(first_mutex, second_mutex);
std::swap(first, second);
```
