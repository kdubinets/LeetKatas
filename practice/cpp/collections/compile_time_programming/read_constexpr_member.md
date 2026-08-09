# Name

Read a Member at Compile Time

# Description

Define the const `area` member function so it multiplies the stored rectangle dimensions and can be called during constant evaluation. The object is already constant-evaluable through its supplied constructor.

# Solution

```cpp
constexpr int area() const {
    return width_ * height_;
}
```
