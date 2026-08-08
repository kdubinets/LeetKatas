# Name

Symmetric Scalar Equality

# Description

Define equality between a Celsius value and its integer representation so both `temperature == number` and `number == temperature` work in C++20. Avoid adding two mirrored overloads.

# Solution

```cpp
friend bool operator==(Celsius temperature, int value) {
    return temperature.value == value;
}
```
