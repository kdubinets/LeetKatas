struct FlagReset {
    bool& flag;

    ~FlagReset() {
        flag = false;
    }
};

template <class Function>
void solve(bool& active, Function operation) {
    active = true;
    // Finish: arrange for active to become false on every exit, then run the operation
}
