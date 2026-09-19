#!/usr/bin/env python3
"""Validate recorded monotonic-structure solutions against brute-force oracles."""

import os, re, shlex, subprocess, tempfile
from pathlib import Path

COLLECTION = Path(__file__).resolve().parents[1] / "collections/b_level/monotonic_stack_and_deque_idioms"

HARNESS = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <string>
#include <vector>
long long checks = 0;
template<class A, class B> void same(const A& a, const B& b, const char* message) {
    ++checks; if (a != b) { std::cerr << message << '\n'; std::exit(1); }
}
std::string normalized(std::string value) {
    auto first = value.find_first_not_of('0');
    return first == std::string::npos ? "0" : value.substr(first);
}
std::string digit_oracle(const std::string& digits, std::size_t remove) {
    std::string best;
    const std::size_t keep = digits.size() - remove;
    for (std::size_t mask = 0; mask < (std::size_t{1} << digits.size()); ++mask) {
        std::size_t bits = 0;
        for (std::size_t copy = mask; copy != 0; copy >>= 1) bits += copy & 1U;
        if (bits != keep) continue;
        std::string candidate;
        for (std::size_t i = 0; i < digits.size(); ++i) if ((mask >> i) & 1U) candidate += digits[i];
        candidate = normalized(candidate);
        if (best.empty() || candidate.size() < best.size() ||
            (candidate.size() == best.size() && candidate < best)) best = candidate;
    }
    return best;
}
void test_values(const std::vector<int>& values) {
    std::vector<std::optional<std::size_t>> next(values.size()), previous(values.size());
    std::vector<std::size_t> spans(values.size());
    for (std::size_t i = 0; i < values.size(); ++i) {
        for (std::size_t j = i + 1; j < values.size(); ++j)
            if (values[j] > values[i]) { next[i] = j; break; }
        for (std::size_t j = i; j-- > 0;)
            if (values[j] < values[i]) { previous[i] = j; break; }
        std::size_t left = i;
        while (left > 0 && values[left - 1] <= values[i]) --left;
        spans[i] = i - left + 1;
    }
    same(next_greater_indices::next_greater_indices(values), next, "next greater");
    same(previous_smaller_indices::previous_smaller_indices(values), previous, "previous smaller");
    same(stock_span_lengths::stock_span_lengths(values), spans, "span");
    for (std::size_t width = 1; width <= values.size(); ++width) {
        std::vector<int> maxima;
        for (std::size_t first = 0; first + width <= values.size(); ++first)
            maxima.push_back(*std::max_element(values.begin() + first, values.begin() + first + width));
        same(sliding_window_maximum::sliding_window_maximum(values, width), maxima, "window maximum");
    }
    long long rectangle = 0;
    for (std::size_t left = 0; left < values.size(); ++left) {
        int height = values[left] + 2;
        for (std::size_t right = left; right < values.size(); ++right) {
            height = std::min(height, values[right] + 2);
            rectangle = std::max(rectangle, static_cast<long long>(height) *
                                            static_cast<long long>(right - left + 1));
        }
    }
    std::vector<int> heights; for (int value : values) heights.push_back(value + 2);
    same(largest_rectangle_area::largest_rectangle_area(heights), rectangle, "rectangle");
    for (long long target = 1; target <= 8; ++target) {
        std::optional<std::size_t> shortest;
        for (std::size_t left = 0; left < values.size(); ++left) {
            long long sum = 0;
            for (std::size_t right = left; right < values.size(); ++right) {
                sum += values[right];
                if (sum >= target) {
                    std::size_t length = right - left + 1;
                    shortest = shortest ? std::min(*shortest, length) : length;
                }
            }
        }
        same(shortest_subarray_at_least_target::shortest_subarray_at_least_target(values, target), shortest, "shortest subarray");
    }
}
int main() {
    for (std::size_t size = 0; size <= 7; ++size) {
        std::size_t count = 1; for (std::size_t i = 0; i < size; ++i) count *= 5;
        for (std::size_t code = 0; code < count; ++code) {
            std::size_t rest = code; std::vector<int> values(size);
            for (int& value : values) { value = static_cast<int>(rest % 5) - 2; rest /= 5; }
            test_values(values);
        }
    }
    for (std::size_t size = 1; size <= 7; ++size) {
        std::size_t count = 1; for (std::size_t i = 0; i < size; ++i) count *= 4;
        for (std::size_t code = 0; code < count; ++code) {
            std::size_t rest = code; std::string digits(size, '0');
            for (char& digit : digits) { digit += rest % 4; rest /= 4; }
            for (std::size_t remove = 0; remove <= size; ++remove)
                same(smallest_digits_after_removal::smallest_digits_after_removal(digits, remove),
                     digit_oracle(digits, remove), "digit removal");
        }
    }
    std::cout << "Monotonic runtime checks passed: " << checks << '\n';
}
"""

def completed(name):
    source=(COLLECTION/f"{name}.cpp").read_text(); metadata=(COLLECTION/f"{name}.md").read_text()
    solution=re.findall(r"^```cpp\n(.*?)^```$",metadata,re.M|re.S)
    done,count=re.subn(r"^([ \t]*)// Finish: .*?$",lambda m:"\n".join(m[1]+x for x in solution[0].rstrip().splitlines()),source,flags=re.M)
    if len(solution)!=1 or count!=1: raise ValueError(name)
    includes=re.findall(r"^#include .*?$",done,re.M); done=re.sub(r"^#include .*?\n","",done,flags=re.M)
    return "\n".join(includes)+f"\nnamespace {name} {{\n"+done+"}\n"

def main():
    source="\n".join(completed(x) for x in (COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
    with tempfile.TemporaryDirectory(prefix="leetkatas-monotonic-") as directory:
        executable=Path(directory)/"checks"
        subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(executable)],input=source,text=True,check=True,timeout=120)
        subprocess.run([str(executable)],check=True,timeout=120)
if __name__ == "__main__": main()
