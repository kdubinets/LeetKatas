# Name

Limit Work with a Semaphore

# Description

Acquire one permit from the supplied counting semaphore, invoke a non-throwing function, and release the permit afterward. This covers bounded concurrent admission without adding exception-cleanup design to the task.

# Solution

```cpp
permits.acquire();
work();
permits.release();
```
