# Name

Define Custom Key Equality

# Description

Implement an equality policy for keys identified by organization and name while ignoring cached permissions. The selected fields are the same ones an accompanying hash policy would need to hash.

# Solution

```cpp
return left.organization == right.organization && left.name == right.name;
```
