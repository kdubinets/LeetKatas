#include <cstddef>

// Finish: return the compile-time bound of any referenced built-in array

int main() {
    int values[6]{};
    return array_length(values) == 6 ? 0 : 1;
}
