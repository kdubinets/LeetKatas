#include <memory>
#include <string>

struct Record {
    std::string name;
    int score;
};

std::unique_ptr<Record> solve(const std::unique_ptr<Record>& source) {
    // Finish: return an independently owned copy of the record, or an empty owner when source is empty
}
