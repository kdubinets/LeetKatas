#include <tuple>

struct Point {
    int x;
    int y;
};

struct NearOrigin {
    bool operator()(Point left, Point right) const {
        // Finish: order by squared distance from the origin, then x, then y
    }
};
