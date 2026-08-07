#include <memory>
#include <string>

struct Record {
    std::string name;
    int score;

    Record(const std::string& name_value, int score_value)
        : name(name_value), score(score_value) {}
};

std::unique_ptr<Record> solve(const std::string& name, int score) {
    // Finish: create and return one exclusively owned record from these constructor arguments
}
