# Name

Validate an Indexed Weekday

# Description

Return whether occurrence `index` of a valid weekday exists in a valid year and month. The index is in the calendar API's representable range of 1 through 5; for example, some months do not contain a fifth occurrence of a weekday.

# Solution

```cpp
return (value / weekday[index]).ok();
```
