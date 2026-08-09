struct Point {
    int x;
    int y;
};

struct Label {
    Point position;
    bool visible;
};

Label solve(int x, int y) {
    // Finish: create a visible label at the specified coordinates using named members
}

int main() {
    const auto value = solve(2, 5);
    return value.position.x == 2 && value.position.y == 5 && value.visible ? 0 : 1;
}
