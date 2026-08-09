# Name

Sum an Array at Compile Time

# Description

Return the integer total of a four-element const array using a loop that is valid during constant evaluation. This trains ordinary iterative code inside a `constexpr` function rather than recursive template metaprogramming.

# Solution

```cpp
int total = 0;
for (int value : values) {
    total += value;
}
return total;
```
