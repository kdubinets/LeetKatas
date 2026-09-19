#include <cstddef>
#include <functional>
#include <queue>
#include <tuple>
#include <vector>

using namespace std;

std::vector<int> merge_k_sorted_sequences(const std::vector<std::vector<int>>& sequences) {
    // Pattern: minimum frontier heap of {value, sequence, position}. Seed the first value of each nonempty input; after emitting an entry, add only its successor from the same sequence.

    // Finish: return every input value in nondecreasing order, preserving duplicate multiplicity; each input sequence is nondecreasing, inputs may be empty, and sequences are not modified
}
