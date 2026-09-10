#include <compare>
#include <tuple>

using namespace std;

struct Version {
    int major;
    int minor;
    int patch;

    friend std::strong_ordering operator<=>(Version left, Version right) {
        // Finish: compare major, then minor, then patch numbers
    }
};
