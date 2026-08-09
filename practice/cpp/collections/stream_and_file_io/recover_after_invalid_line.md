# Name

Recover After an Invalid Line

# Description

The supplied `std::istream&` is in a failed state after an invalid formatted extraction within the current line. Restore it, discard the rest of that line, and read an `int` from the next record. Return the integer on success or an empty optional if the retry also fails. This exercise covers stream-state recovery and bounded record skipping.

# Solution

```cpp
input.clear();
input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
int value;
if (input >> value) {
    return value;
}
return std::nullopt;
```
