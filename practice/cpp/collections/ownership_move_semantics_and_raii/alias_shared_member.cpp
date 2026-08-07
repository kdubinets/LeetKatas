#include <memory>
#include <string>

struct Record {
    int id;
    std::string name;
};

std::shared_ptr<const std::string> solve(
    const std::shared_ptr<Record>& owner) {
    // Finish: for this non-null owner, share its lifetime while pointing at its name member
}
