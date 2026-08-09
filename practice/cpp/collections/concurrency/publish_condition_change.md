# Name

Publish a Condition Change

# Description

Set the supplied readiness flag while holding its mutex, release the mutex, and then wake one condition-variable waiter. This trains the state-change side of a predicate wait and avoids waking a waiter only to make it contend for a still-held lock.

# Solution

```cpp
{
    std::lock_guard lock(mutex);
    ready = true;
}
changed.notify_one();
```
