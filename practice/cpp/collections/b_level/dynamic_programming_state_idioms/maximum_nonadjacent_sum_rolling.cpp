#include <algorithm>
#include <vector>

using namespace std;

long long maximum_nonadjacent_sum(const std::vector<int>& values) {
    // Pattern: supplied recurrence with two rolling states. After index i, best(i) = max(best(i - 1), best(i - 2) + values[i]); the states before the scan are both zero.

    // Finish: return the greatest sum obtainable by selecting no two adjacent indices; selecting nothing is allowed, so return 0 for empty or all-negative input; do not modify values, and assume all intermediate and final sums fit in long long
}
