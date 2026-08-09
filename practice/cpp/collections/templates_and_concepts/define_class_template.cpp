#include <string>

// Finish: define a holder whose stored value has the selected template type

int main() {
    Box<std::string> box{"ready"};
    return box.value == "ready" ? 0 : 1;
}
