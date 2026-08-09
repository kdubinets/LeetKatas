# Name

Specify a Template Argument

# Description

Call the provided function template with `double` explicitly selected for its first template parameter. The input type should remain deduced from the integer argument.

# Solution

```cpp
return convert<double>(value);
```
