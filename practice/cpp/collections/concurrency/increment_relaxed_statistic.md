# Name

Increment a Relaxed Statistic

# Description

Increment a supplied atomic event count where only the count itself is shared and no other memory is published or consumed through the operation. This trains relaxed ordering for an independent statistic that still requires an indivisible update.

# Solution

```cpp
count.fetch_add(1, std::memory_order_relaxed);
```
