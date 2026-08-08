# Name

Construct a Duration with Literals

# Description

Return exactly 2.25 seconds as `std::chrono::milliseconds` by composing standard chrono duration literals. This trains readable typed duration constants without raw count scaling.

# Solution

```cpp
using namespace std::chrono_literals;
return 2s + 250ms;
```
