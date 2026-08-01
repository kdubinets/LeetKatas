# Name

Find Lowest Score Record

# Description

Given a nonempty const vector of `Record` objects containing integer IDs and scores, return the ID of the first record whose score is minimal. The input must remain unchanged. This exercise covers selecting an extremum through a member projection.

# Solution

```cpp
return std::ranges::min_element(records, {}, &Record::score)->id;
```
