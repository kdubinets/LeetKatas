consteval int checked_percentage(int value) {
    // Finish: return values from 0 through 100 and make other calls invalid during constant evaluation
}

constexpr int percentage = checked_percentage(75);
static_assert(percentage == 75);
