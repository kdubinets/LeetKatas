# C++ Solution Testing

Keep `solutions/cpp/<id>.cpp` as a LeetCode-compatible snippet: it defines `class Solution` and has no `main` function.

Put its standalone runtime harness in `solutions/tests/cpp/<id>.cpp`. Include standard headers before the solution, then include it with a relative path:

```cpp
#include <cassert>
#include <vector>

#include "../../cpp/15.cpp"

int main() {
    Solution solution;
    assert((solution.threeSum({0, 0, 0}) == std::vector<std::vector<int>>{{0, 0, 0}}));
}
```

Use `assert` and a zero exit status. Normalize or compare as sets when the problem does not prescribe output order. Test the supplied examples, boundaries, and inputs that exercise duplicate handling, overflow, empty state, or other problem-specific risks. Use a small brute-force oracle or randomized cross-check only when it makes the test clearer and remains deterministic.

Run:

```bash
python3 .agents/skills/solve-leetkata-problem/scripts/verify_cpp_solution.py \
  problems/<difficulty>/solutions/cpp/<id>.cpp \
  --test problems/<difficulty>/solutions/tests/cpp/<id>.cpp
```
