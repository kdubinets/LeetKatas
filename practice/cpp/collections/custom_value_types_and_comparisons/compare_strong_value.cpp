#include <compare>

struct Revision {
    int value;

    friend std::strong_ordering operator<=>(Revision left, Revision right) {
        // Finish: compare revisions by their integer values
    }
};
