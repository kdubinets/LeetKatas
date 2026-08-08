#include <compare>

struct Revision {
    int value;

    friend bool operator==(Revision revision, int value) {
        return revision.value == value;
    }

    // Finish: allow ordering against an integer in either operand order
};
