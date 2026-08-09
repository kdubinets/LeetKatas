# Name

Synchronize a Barrier Phase

# Description

Record this participant's arrival at the supplied reusable barrier, perform the supplied non-throwing work that does not depend on other participants, and then wait for the current phase to complete. This trains split arrival and waiting through a barrier arrival token.

# Solution

```cpp
auto arrival = phase.arrive();
independent_work();
phase.wait(std::move(arrival));
```
