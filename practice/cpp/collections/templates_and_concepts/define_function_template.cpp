#include <string>

template <class T>
// Finish: return the larger value without fixing its type in advance

int main() {
    return larger(3, 7) == 7 && larger(std::string{"a"}, std::string{"b"}) == "b" ? 0 : 1;
}
