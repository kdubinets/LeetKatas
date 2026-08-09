# Name

Observe a Stop Request

# Description

Return whether work should continue according to a supplied cooperative cancellation token. The function does not own or initiate cancellation; it only observes the token's current state.

# Solution

```cpp
return !token.stop_requested();
```
