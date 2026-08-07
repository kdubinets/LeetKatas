#include <memory>
#include <utility>
#include <vector>

struct Task {
    int id;
};

void solve(std::vector<std::unique_ptr<Task>>& tasks,
           std::unique_ptr<Task> task) {
    // Finish: append the task by transferring its exclusive ownership into the vector
}
