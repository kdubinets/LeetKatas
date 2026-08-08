# Name

Invoke an Optional Callback

# Description

Given a possibly empty `std::function<void(int)>`, invoke it with the supplied integer only when a target is present. The callback object is read without modification.

# Solution

```cpp
if (callback) {
    callback(value);
}
```
