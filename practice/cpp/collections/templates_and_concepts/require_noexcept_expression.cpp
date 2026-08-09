struct SafeReset {
    void reset() noexcept;
};

struct RiskyReset {
    void reset();
};

template <class T>
// Finish: require reset on a mutable value to be valid and non-throwing

static_assert(NothrowReset<SafeReset>);
static_assert(!NothrowReset<RiskyReset>);
