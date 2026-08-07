# Name

Release a Unique Owner to Legacy Code

# Description

Pass a nonempty resource from `std::unique_ptr<Resource>` to `legacy_adopt`, which assumes responsibility for eventually destroying the raw pointer. Leave the unique pointer empty. This exercise covers explicitly relinquishing ownership at an adopting API boundary.

# Solution

```cpp
legacy_adopt(owner.release());
```
