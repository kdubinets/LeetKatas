#include <cmath>
#include <optional>
#include <set>

struct AbsoluteOrder {
    bool operator()(int left, int right) const {
        return std::abs(left) < std::abs(right);
    }
};

std::optional<int> solve(const std::set<int, AbsoluteOrder>& values, int target) {
    // Finish: return the stored value equivalent to the target under the set's ordering
}
