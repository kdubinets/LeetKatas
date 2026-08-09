class Point {
public:
    // Finish: initialize both coordinates in a form usable during constant evaluation

    constexpr int x() const { return x_; }
    constexpr int y() const { return y_; }

private:
    int x_;
    int y_;
};

static_assert(Point{2, 3}.x() == 2);
static_assert(Point{2, 3}.y() == 3);
