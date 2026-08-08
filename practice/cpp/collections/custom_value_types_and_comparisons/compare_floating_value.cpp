#include <compare>

struct Measurement {
    double value;

    friend std::partial_ordering operator<=>(Measurement left, Measurement right) {
        // Finish: compare the stored measurements while preserving unordered results
    }
};
