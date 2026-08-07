# Name

Clone a Unique Record

# Description

Given a const `std::unique_ptr<Record>`, return a separately allocated copy of its record or an empty unique pointer when the source is empty. The source and any existing record must remain unchanged. This exercise covers explicit deep copying of nullable exclusive ownership.

# Solution

```cpp
if (!source) {
    return nullptr;
}
return std::make_unique<Record>(*source);
```
