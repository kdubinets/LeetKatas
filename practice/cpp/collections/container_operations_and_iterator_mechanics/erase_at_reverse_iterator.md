# Name

Erase at a Reverse Iterator

# Description

Erase the element selected by the valid dereferenceable const reverse iterator `position` from `values`, then return the forward iterator following the erased element. The iterator belongs to `values`. This exercise covers the offset relationship between a reverse iterator and its forward base iterator when calling a container interface that accepts forward iterators.

# Solution

```cpp
return values.erase(std::next(position).base());
```
