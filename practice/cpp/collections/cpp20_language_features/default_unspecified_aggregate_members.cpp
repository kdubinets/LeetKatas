struct Counters {
    int accepted = 0;
    int rejected = 0;
    int pending = 0;
};

Counters solve(int pending) {
    // Finish: set only pending explicitly and zero-initialize the other counters
}

int main() {
    const auto value = solve(4);
    return value.accepted == 0 && value.rejected == 0 && value.pending == 4 ? 0 : 1;
}
