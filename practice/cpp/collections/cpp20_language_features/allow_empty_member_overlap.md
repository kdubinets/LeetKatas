# Name

Allow an Empty Member to Overlap

# Description

Declare an `EmptyPolicy` data member named `policy` and apply the C++20 attribute that permits an empty member to overlap another member's address. Leave `value` as the following member.

# Solution

```cpp
[[no_unique_address]] EmptyPolicy policy;
```
