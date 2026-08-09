# Name

Join Before Reading

# Description

Wait for a worker thread to finish before returning the integer it writes. The worker owns no data and borrows the local result only until it is joined. This exercise covers explicit thread completion and the synchronization that makes the produced value safe to read.

# Solution

```cpp
worker.join();
return result;
```
