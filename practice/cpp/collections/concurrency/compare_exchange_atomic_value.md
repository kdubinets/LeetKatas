# Name

Compare and Exchange an Atomic Value

# Description

Attempt one strong conditional replacement of an atomic integer. Return whether replacement succeeded; on failure, write the actually observed value back through the caller's `expected` reference. This trains the two-way expected-parameter contract without requiring a retry loop.

# Solution

```cpp
return value.compare_exchange_strong(expected, desired);
```
