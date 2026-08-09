# Name

Run a Stop Callback

# Description

Register a callback on a token from the supplied stop source so it sets a local Boolean, request cancellation while the registration remains alive, and return the Boolean. This covers synchronous stop callbacks without starting a thread.

# Solution

```cpp
std::stop_callback callback(source.get_token(), [&called] { called = true; });
source.request_stop();
return called;
```
