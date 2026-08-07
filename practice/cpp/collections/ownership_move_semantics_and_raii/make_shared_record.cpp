#include <memory>

struct Record {
    explicit Record(int identifier) : id(identifier) {}
    int id;
};

std::shared_ptr<Record> solve(int id) {
    // Finish: create and return a shared record from this constructor argument
}
