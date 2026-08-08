# Name

Custom Value Equality

# Description

Define equality for `Account` using its stable ID and display name while excluding the derived cached score. This trains explicit selection of equality-bearing fields.

# Solution

```cpp
return left.id == right.id && left.display_name == right.display_name;
```
