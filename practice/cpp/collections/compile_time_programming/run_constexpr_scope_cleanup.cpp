struct ScopeIncrement {
    int* count;

    // Finish: increment the referenced counter when this object leaves scope, including during constant evaluation
};

consteval int count_cleanup() {
    int count = 0;
    {
        ScopeIncrement guard{&count};
    }
    return count;
}

static_assert(count_cleanup() == 1);
