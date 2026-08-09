#include <vector>

struct Numbers {
    std::vector<int> values;

    const std::vector<int>& view() const {
        return values;
    }
};

Numbers load_numbers() {
    return {{2, 4, 6}};
}

int solve() {
    int total = 0;
    // Finish: keep the loaded owner named while summing the values exposed by its view
    return total;
}

int main() {
    return solve() == 12 ? 0 : 1;
}
