#!/usr/bin/env python3
"""Validate recorded sequence-scan solutions against deterministic oracles."""

import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


COLLECTION = (
    Path(__file__).resolve().parents[1]
    / "collections/b_level/sequence_scanning_and_window_idioms"
)

HARNESS = r"""
#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <random>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

long long checks = 0;

void require(bool condition, const char* message) {
    ++checks;
    if (!condition) {
        std::cerr << message << '\n';
        std::exit(1);
    }
}

template<class Left, class Right>
void assert_equal(const Left& actual, const Right& expected, const char* message) {
    require(actual == expected, message);
}

long long maximum_window_sum_oracle(
    const std::vector<int>& values,
    std::size_t width) {
    if (width == 0 || width > values.size()) return 0;
    long long best = 0;
    bool initialized = false;
    for (std::size_t left = 0; left + width <= values.size(); ++left) {
        long long sum = 0;
        for (std::size_t index = left; index < left + width; ++index) {
            sum += values[index];
        }
        if (!initialized || sum > best) best = sum;
        initialized = true;
    }
    return best;
}

std::size_t distinct_window_count_oracle(
    const std::vector<int>& values,
    std::size_t width) {
    if (width == 0 || width > values.size()) return 0;
    std::size_t count = 0;
    for (std::size_t left = 0; left + width <= values.size(); ++left) {
        std::set<int> seen(
            values.begin() + static_cast<std::ptrdiff_t>(left),
            values.begin() + static_cast<std::ptrdiff_t>(left + width));
        if (seen.size() == width) ++count;
    }
    return count;
}

std::size_t anagram_count_oracle(
    const std::string& text,
    const std::string& pattern) {
    if (pattern.empty() || pattern.size() > text.size()) return 0;
    std::array<int, 26> needed{};
    for (char value : pattern) ++needed[value - 'a'];
    std::size_t count = 0;
    for (std::size_t left = 0; left + pattern.size() <= text.size(); ++left) {
        std::array<int, 26> found{};
        for (std::size_t index = left; index < left + pattern.size(); ++index) {
            ++found[text[index] - 'a'];
        }
        if (found == needed) ++count;
    }
    return count;
}

std::size_t longest_unique_oracle(const std::string& text) {
    std::size_t best = 0;
    for (std::size_t left = 0; left < text.size(); ++left) {
        std::array<bool, 256> seen{};
        for (std::size_t right = left; right < text.size(); ++right) {
            const auto value = static_cast<unsigned char>(text[right]);
            if (seen[value]) break;
            seen[value] = true;
            best = std::max(best, right - left + 1);
        }
    }
    return best;
}

std::size_t shortest_positive_sum_oracle(
    const std::vector<int>& values,
    long long target) {
    std::size_t best = values.size() + 1;
    for (std::size_t left = 0; left < values.size(); ++left) {
        long long sum = 0;
        for (std::size_t right = left; right < values.size(); ++right) {
            sum += values[right];
            if (sum >= target) {
                best = std::min(best, right - left + 1);
                break;
            }
        }
    }
    return best == values.size() + 1 ? 0 : best;
}

std::size_t longest_distinct_limit_oracle(
    const std::string& text,
    std::size_t limit) {
    std::size_t best = 0;
    for (std::size_t left = 0; left < text.size(); ++left) {
        std::set<unsigned char> distinct;
        for (std::size_t right = left; right < text.size(); ++right) {
            distinct.insert(static_cast<unsigned char>(text[right]));
            if (distinct.size() > limit) break;
            best = std::max(best, right - left + 1);
        }
    }
    return best;
}

long long maximum_container_oracle(const std::vector<int>& heights) {
    long long best = 0;
    for (std::size_t left = 0; left < heights.size(); ++left) {
        for (std::size_t right = left + 1; right < heights.size(); ++right) {
            best = std::max(
                best,
                static_cast<long long>(right - left) *
                    std::min(heights[left], heights[right]));
        }
    }
    return best;
}

std::size_t target_sum_count_oracle(
    const std::vector<int>& values,
    long long target) {
    std::size_t count = 0;
    for (std::size_t left = 0; left < values.size(); ++left) {
        long long sum = 0;
        for (std::size_t right = left; right < values.size(); ++right) {
            sum += values[right];
            if (sum == target) ++count;
        }
    }
    return count;
}

std::size_t longest_balanced_oracle(const std::vector<int>& values) {
    std::size_t best = 0;
    for (std::size_t left = 0; left < values.size(); ++left) {
        int balance = 0;
        for (std::size_t right = left; right < values.size(); ++right) {
            balance += values[right] == 0 ? -1 : 1;
            if (balance == 0) best = std::max(best, right - left + 1);
        }
    }
    return best;
}

int main() {
    std::mt19937 random(20260919);
    for (int trial = 0; trial < 10000; ++trial) {
        std::vector<int> values(random() % 17);
        for (int& value : values) {
            value = static_cast<int>(random() % 21) - 10;
        }
        const std::size_t width = random() % (values.size() + 3);
        assert_equal(fixed_window_maximum_sum::maximum_window_sum(values, width),
              maximum_window_sum_oracle(values, width), "maximum window sum");
        assert_equal(fixed_window_all_distinct_count::count_all_distinct_windows(
                  values, width),
              distinct_window_count_oracle(values, width),
              "all-distinct windows");

        std::string text(random() % 18, 'a');
        std::string pattern(random() % 8, 'a');
        for (char& value : text) value = static_cast<char>('a' + random() % 5);
        for (char& value : pattern) value = static_cast<char>('a' + random() % 5);
        assert_equal(fixed_window_anagram_match_count::count_anagram_windows(text, pattern),
              anagram_count_oracle(text, pattern), "anagram windows");
        assert_equal(longest_unique_substring::longest_unique_substring_length(text),
              longest_unique_oracle(text), "longest unique substring");
        const std::size_t distinct_limit = random() % 8;
        assert_equal(longest_at_most_k_distinct::longest_at_most_k_distinct_length(
                  text, distinct_limit),
              longest_distinct_limit_oracle(text, distinct_limit),
              "distinct limit");

        std::vector<int> positive = values;
        for (int& value : positive) value = std::abs(value) + 1;
        const long long positive_target = random() % 50 + 1;
        assert_equal(minimum_length_sum_at_least_target::minimum_length_sum_at_least_target(
                  positive, positive_target),
              shortest_positive_sum_oracle(positive, positive_target),
              "minimum positive-sum window");

        auto sorted = values;
        std::sort(sorted.begin(), sorted.end());
        const long long pair_target = static_cast<int>(random() % 31) - 15;
        const auto pair = two_sum_sorted_converging::two_sum_sorted_indices(
            sorted, pair_target);
        bool pair_exists = false;
        for (std::size_t left = 0; left < sorted.size(); ++left) {
            for (std::size_t right = left + 1; right < sorted.size(); ++right) {
                pair_exists = pair_exists ||
                    static_cast<long long>(sorted[left]) + sorted[right] == pair_target;
            }
        }
        assert_equal(pair.has_value(), pair_exists, "sorted two-sum presence");
        if (pair) {
            require(pair->first < pair->second && pair->second < sorted.size(),
                    "sorted two-sum indices");
            assert_equal(static_cast<long long>(sorted[pair->first]) + sorted[pair->second],
                  pair_target, "sorted two-sum value");
        }

        std::vector<int> heights = values;
        for (int& height : heights) height = std::abs(height);
        assert_equal(maximum_container_area::maximum_container_area(heights),
              maximum_container_oracle(heights), "container area");

        const std::size_t split = sorted.empty() ? 0 : random() % (sorted.size() + 1);
        std::vector<int> left(sorted.begin(),
                              sorted.begin() + static_cast<std::ptrdiff_t>(split));
        std::vector<int> right(sorted.begin() + static_cast<std::ptrdiff_t>(split),
                               sorted.end());
        left.resize(sorted.size());
        merge_sorted_sequences_from_end::merge_sorted_into_first(left, split, right);
        assert_equal(left, sorted, "backward sorted merge");

        auto compacted = sorted;
        const std::size_t original_size = compacted.size();
        const std::size_t retained =
            compact_sorted_duplicates::compact_sorted_duplicates(compacted);
        auto unique = sorted;
        unique.erase(std::unique(unique.begin(), unique.end()), unique.end());
        assert_equal(compacted.size(), original_size, "compaction size");
        require(retained == unique.size() &&
                    std::equal(unique.begin(), unique.end(), compacted.begin()),
                "compaction prefix");

        auto moved = values;
        move_zeroes_in_place::move_zeroes_to_end(moved);
        std::vector<int> expected_moved;
        for (int value : values) if (value != 0) expected_moved.push_back(value);
        expected_moved.resize(values.size(), 0);
        assert_equal(moved, expected_moved, "move zeroes");

        auto partitioned = values;
        const std::size_t boundary =
            partition_negatives_first::partition_negatives_first(partitioned);
        require(boundary <= partitioned.size(), "partition boundary");
        for (std::size_t index = 0; index < boundary; ++index) {
            require(partitioned[index] < 0, "negative partition region");
        }
        for (std::size_t index = boundary; index < partitioned.size(); ++index) {
            require(partitioned[index] >= 0, "nonnegative partition region");
        }
        auto partitioned_sorted = partitioned;
        std::sort(partitioned_sorted.begin(), partitioned_sorted.end());
        auto values_sorted = values;
        std::sort(values_sorted.begin(), values_sorted.end());
        assert_equal(partitioned_sorted, values_sorted, "partition multiplicity");

        const long long sum_target = static_cast<int>(random() % 31) - 15;
        assert_equal(count_subarrays_with_target_sum::count_subarrays_with_target_sum(
                  values, sum_target),
              target_sum_count_oracle(values, sum_target),
              "target-sum ranges");

        std::vector<int> binary(values.size());
        for (int& value : binary) value = static_cast<int>(random() % 2);
        assert_equal(longest_balanced_binary_subarray::longest_balanced_binary_subarray(binary),
              longest_balanced_oracle(binary), "balanced binary range");

        std::vector<std::pair<std::size_t, std::size_t>> queries;
        if (!values.empty()) {
            for (std::size_t index = 0; index < random() % 12; ++index) {
                std::size_t first = random() % values.size();
                std::size_t last = random() % values.size();
                if (first > last) std::swap(first, last);
                queries.emplace_back(first, last);
            }
        }
        std::vector<long long> query_answers;
        for (const auto& [first, last] : queries) {
            long long sum = 0;
            for (std::size_t index = first; index <= last; ++index) {
                sum += values[index];
            }
            query_answers.push_back(sum);
        }
        assert_equal(range_sum_queries_from_prefixes::range_sum_queries(values, queries),
              query_answers, "range sums");

        std::vector<apply_closed_range_additions::RangeAddition> updates;
        std::vector<long long> added(values.size(), 0);
        if (!values.empty()) {
            for (std::size_t index = 0; index < random() % 12; ++index) {
                std::size_t first = random() % values.size();
                std::size_t last = random() % values.size();
                if (first > last) std::swap(first, last);
                const long long delta = static_cast<int>(random() % 21) - 10;
                updates.push_back({first, last, delta});
                for (std::size_t position = first; position <= last; ++position) {
                    added[position] += delta;
                }
            }
        }
        assert_equal(apply_closed_range_additions::apply_closed_range_additions(
                  values.size(), updates),
              added, "closed range additions");

        const int search_target = static_cast<int>(random() % 31) - 15;
        const auto exact = binary_search_exact::binary_search_exact_index(
            sorted, search_target);
        const bool exact_exists = std::binary_search(
            sorted.begin(), sorted.end(), search_target);
        assert_equal(exact.has_value(), exact_exists, "exact binary-search presence");
        if (exact) {
            require(*exact < sorted.size() && sorted[*exact] == search_target,
                    "exact binary-search index");
        }
        const std::size_t lower = static_cast<std::size_t>(
            std::lower_bound(sorted.begin(), sorted.end(), search_target) -
            sorted.begin());
        assert_equal(binary_search_first_not_less::first_not_less_index(
                  sorted, search_target),
              lower, "lower boundary");
        const auto upper_iterator =
            std::upper_bound(sorted.begin(), sorted.end(), search_target);
        const auto last =
            upper_iterator == sorted.begin()
                ? std::optional<std::size_t>{}
                : std::optional<std::size_t>{static_cast<std::size_t>(
                      upper_iterator - sorted.begin() - 1)};
        assert_equal(binary_search_last_not_greater::last_not_greater_index(
                  sorted, search_target),
              last, "upper boundary");
    }
    std::cout << "Sequence-scan runtime checks passed: " << checks << '\n';
}
"""


def completed_source(basename):
    source = (COLLECTION / f"{basename}.cpp").read_text()
    metadata = (COLLECTION / f"{basename}.md").read_text()
    solutions = re.findall(
        r"^```cpp\n(.*?)^```$", metadata, re.MULTILINE | re.DOTALL
    )
    if len(solutions) != 1:
        raise ValueError(f"Expected one solution: {basename}")
    completed, count = re.subn(
        r"^([ \t]*)// Finish: .*?$",
        lambda match: "\n".join(
            match[1] + line for line in solutions[0].rstrip().splitlines()
        ),
        source,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(f"Expected one Finish marker: {basename}")
    includes = re.findall(r"^#include .*?$", completed, re.MULTILINE)
    completed = re.sub(r"^#include .*?\n", "", completed, flags=re.MULTILINE)
    return "\n".join(includes) + f"\nnamespace {basename} {{\n" + completed + "}\n"


def main():
    basenames = (COLLECTION / "exercise_order.md").read_text().splitlines()
    source = "\n".join(map(completed_source, basenames)) + HARNESS
    with tempfile.TemporaryDirectory(prefix="leetkatas-sequence-scan-") as directory:
        executable = Path(directory) / "checks"
        subprocess.run(
            shlex.split(os.environ.get("CXX", "g++"))
            + [
                "-std=c++20",
                "-Wall",
                "-Wextra",
                "-Werror",
                "-O1",
                "-g",
                "-fsanitize=address,undefined",
                "-fno-omit-frame-pointer",
                "-D_GLIBCXX_ASSERTIONS",
                "-x",
                "c++",
                "-",
                "-o",
                str(executable),
            ],
            input=source,
            text=True,
            check=True,
            timeout=120,
        )
        environment = os.environ.copy()
        environment["ASAN_OPTIONS"] = "detect_leaks=0"
        subprocess.run(
            [str(executable)], check=True, timeout=120, env=environment
        )


if __name__ == "__main__":
    main()
