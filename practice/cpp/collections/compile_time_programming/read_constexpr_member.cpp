class Rectangle {
public:
    constexpr Rectangle(int width, int height)
        : width_(width), height_(height) {}

    // Finish: return the area in a form usable during constant evaluation

private:
    int width_;
    int height_;
};

static_assert(Rectangle{6, 7}.area() == 42);
