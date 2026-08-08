# Name

Shift Calendar Fields by Months

# Description

Shift a `year_month_day` by a signed number of calendar months while retaining its numbered day field. The returned date may be invalid when the destination month lacks that day; do not silently clamp it.

# Solution

```cpp
return date + offset;
```
