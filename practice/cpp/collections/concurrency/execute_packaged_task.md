# Name

Execute a Packaged Task

# Description

Obtain the future associated with a supplied move-only packaged task, transfer the task into a worker thread, join the worker, and return the future. The callable and its shared result state are already encapsulated by the task.

# Solution

```cpp
auto future = task.get_future();
std::thread worker(std::move(task));
worker.join();
return future;
```
