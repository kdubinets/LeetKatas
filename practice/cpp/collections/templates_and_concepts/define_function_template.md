# Name

Define a Function Template

# Description

Define `larger` for two const references of one deduced type and return a const reference to the greater value. The call sites exercise both integers and strings.

# Solution

```cpp
const T& larger(const T& left, const T& right) {
    return left < right ? right : left;
}
```
