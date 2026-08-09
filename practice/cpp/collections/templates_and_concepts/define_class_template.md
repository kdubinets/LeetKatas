# Name

Define a Class Template

# Description

Define aggregate class template `Box` with one public member named `value` whose type is the class's type parameter. It must support the shown explicit specialization of the class argument.

# Solution

```cpp
template <class T>
struct Box {
    T value;
};
```
