# Name

Set a Last Write Time

# Description

Set a filesystem entry's modification time to the supplied `file_time_type` value without throwing. Report success or failure through the caller-provided `std::error_code`.

# Solution

```cpp
std::filesystem::last_write_time(value, time, error);
```
