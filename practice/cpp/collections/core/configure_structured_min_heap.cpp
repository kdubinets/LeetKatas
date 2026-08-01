#include <queue>
#include <vector>

struct Task {
    int priority;
    int id;
};

struct TaskOrder {
    bool operator()(const Task& left, const Task& right) const {
        // Finish: make the priority queue's top task have the lowest priority, breaking ties with the lowest id
    }
};

using TaskQueue = std::priority_queue<Task, std::vector<Task>, TaskOrder>;
