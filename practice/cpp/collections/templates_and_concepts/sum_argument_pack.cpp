template <class... Values>
int sum_values(Values... values) {
    // Finish: add every value to an integer zero
}

int main() {
    return sum_values() == 0 && sum_values(1, 2, 3) == 6 ? 0 : 1;
}
