# Name

Throw a Reported System Error

# Description

Call an operation that reports failure through an output `std::error_code`. When it fails, translate that value into `std::system_error` with the context message `writing data failed`; otherwise return normally.

# Solution

```cpp
std::error_code error;
write_data(error);
if (error) {
    throw std::system_error{error, "writing data failed"};
}
```
