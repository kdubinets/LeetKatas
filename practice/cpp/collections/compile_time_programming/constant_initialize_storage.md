# Name

Guarantee Constant Initialization

# Description

Define the externally linked mutable integer `counter` with value `7` and require it to be initialized during static initialization. The object remains writable at runtime; this exercise distinguishes guaranteed constant initialization from a const object.

# Solution

```cpp
constinit int counter = 7;
```
