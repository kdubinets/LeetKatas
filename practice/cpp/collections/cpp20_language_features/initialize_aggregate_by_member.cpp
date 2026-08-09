struct Options {
    int retries = 1;
    bool verbose = false;
    int timeout = 10;
};

Options solve() {
    // Finish: create options with verbose enabled and timeout set to 30
}

int main() {
    const auto value = solve();
    return value.retries == 1 && value.verbose && value.timeout == 30 ? 0 : 1;
}
