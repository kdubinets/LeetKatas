# Name

Wrap a Resource with a Deleter

# Description

Acquire a raw resource and return it as `ResourceOwner`, configuring its stateful deleter with the supplied release-channel integer. This exercise covers binding a nonstandard resource-release operation and its state to exclusive ownership.

# Solution

```cpp
return ResourceOwner{acquire_resource(id), ResourceDeleter{release_channel}};
```
