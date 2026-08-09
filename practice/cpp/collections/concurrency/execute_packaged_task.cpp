#include <future>
#include <thread>
#include <utility>

std::future<int> run(std::packaged_task<int()> task) {
    // Finish: connect to the task result, transfer the task to a worker, wait for execution, and return the future
}
