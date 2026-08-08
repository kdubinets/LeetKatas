# Name

Default Value Equality

# Description

Add equality to a two-field identifier so all data members participate in memberwise value equality. Define the operator as a non-member associated with the type without manually repeating the fields.

# Solution

```cpp
friend bool operator==(const UserId&, const UserId&) = default;
```
