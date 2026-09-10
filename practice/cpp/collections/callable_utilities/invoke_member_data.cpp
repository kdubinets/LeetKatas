#include <functional>
#include <string>

using namespace std;

struct Record {
    std::string name;
    std::string label;
};

const std::string& solve(const Record& record, std::string Record::*member) {
    // Finish: return the selected string member of record without copying it
}
