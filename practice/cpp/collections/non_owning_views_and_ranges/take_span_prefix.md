# Name

Take a Span Prefix

# Description

Given a read-only dynamic span and a valid runtime count no greater than its size, return a span over exactly the first `count` elements. No elements are copied. This exercise covers runtime-sized span prefixes.

# Solution

```cpp
return values.first(count);
```
