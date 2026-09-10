#include <algorithm>
#include <functional>
#include <vector>

using namespace std;

struct Sum {
    Sum() = default;
    Sum(const Sum&) = delete;

    int total = 0;

    void operator()(int value) {
        total += value;
    }
};

void solve(const std::vector<int>& values, Sum& sum) {
    // Finish: apply sum to every value without trying to copy it
}
