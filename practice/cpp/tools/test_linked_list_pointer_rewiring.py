#!/usr/bin/env python3
"""Compile recorded solutions in temporary storage and check node topology."""

import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


COLLECTION = (
    Path(__file__).resolve().parents[1]
    / "collections/b_level/linked_list_pointer_rewiring"
)

HARNESS = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <iterator>
#include <random>
#include <string>
#include <vector>

std::size_t checks = 0;
void require(bool condition, const char* message) {
    ++checks;
    if (!condition) {
        std::cerr << message << '\n';
        std::exit(1);
    }
}

template<class Node>
void check_chain(Node* head, const std::vector<Node*>& expected) {
    for (Node* node : expected) {
        require(head == node, "Wrong node identity or order");
        head = head->next;
    }
    require(head == nullptr, "Extra node or unintended cycle");
}

template<class Node>
struct Pool {
    std::vector<Node> storage;
    std::vector<Node*> order;
    std::vector<int> original;

    Pool(const std::vector<int>& values, std::mt19937& random)
        : storage(values.size()), original(values.size()) {
        for (Node& node : storage) order.push_back(&node);
        std::shuffle(order.begin(), order.end(), random);
        for (std::size_t i = 0; i < order.size(); ++i) {
            order[i]->value = values[i];
            order[i]->next = i + 1 < order.size() ? order[i + 1] : nullptr;
        }
        for (std::size_t i = 0; i < storage.size(); ++i)
            original[i] = storage[i].value;
    }

    Node* head() { return order.empty() ? nullptr : order.front(); }
    void check_values() const {
        for (std::size_t i = 0; i < storage.size(); ++i)
            require(storage[i].value == original[i], "Changed node payload");
    }
    void check(Node* result, const std::vector<Node*>& expected) const {
        check_chain(result, expected);
        check_values();
    }
};
"""

CASES = r"""
void test_one(const std::vector<int>& values, std::mt19937& random) {
    {
        using namespace reverse_entire_list;
        Pool<Node> pool(values, random);
        auto expected = pool.order;
        std::reverse(expected.begin(), expected.end());
        pool.check(reverse_entire_list::reverse_entire_list(pool.head()), expected);
    }
    for (int target = -2; target <= 2; ++target) {
        using namespace remove_matching_nodes;
        Pool<Node> pool(values, random);
        std::vector<Node*> expected;
        for (Node* node : pool.order)
            if (node->value != target) expected.push_back(node);
        pool.check(remove_matching_nodes::remove_matching_nodes(pool.head(), target), expected);
    }
#ifdef HAS_stable_partition_nodes_by_sign
    {
        using namespace stable_partition_nodes_by_sign;
        Pool<Node> pool(values, random);
        auto expected = pool.order;
        std::stable_partition(expected.begin(), expected.end(),
                              [](Node* node) { return node->value < 0; });
        pool.check(stable_partition_nodes_by_sign::stable_partition_nodes_by_sign(pool.head()), expected);
    }
#endif
#ifdef HAS_swap_adjacent_node_pairs
    {
        using namespace swap_adjacent_node_pairs;
        Pool<Node> pool(values, random);
        auto expected = pool.order;
        for (std::size_t i = 0; i + 1 < expected.size(); i += 2)
            std::swap(expected[i], expected[i + 1]);
        pool.check(swap_adjacent_node_pairs::swap_adjacent_node_pairs(pool.head()), expected);
    }
#endif
#ifdef HAS_reverse_node_segment
    for (std::size_t first = 0; first < values.size(); ++first) {
        for (std::size_t last = first; last < values.size(); ++last) {
            using namespace reverse_node_segment;
            Pool<Node> pool(values, random);
            auto expected = pool.order;
            std::reverse(expected.begin() + first, expected.begin() + last + 1);
            pool.check(reverse_node_segment::reverse_node_segment(pool.head(), first, last), expected);
        }
    }
#endif
}

void test_merge(std::vector<int> left, std::vector<int> right, std::mt19937& random) {
    using namespace merge_sorted_node_chains;
    std::sort(left.begin(), left.end());
    std::sort(right.begin(), right.end());
    Pool<Node> a(left, random), b(right, random);
    std::vector<Node*> expected;
    std::merge(a.order.begin(), a.order.end(), b.order.begin(), b.order.end(),
               std::back_inserter(expected),
               [](Node* x, Node* y) { return x->value < y->value; });
    check_chain(merge_sorted_node_chains::merge_sorted_node_chains(a.head(), b.head()), expected);
    a.check_values();
    b.check_values();
}

int main() {
    std::mt19937 random(20260918);
    for (std::size_t size = 0; size <= 7; ++size) {
        std::size_t combinations = 1;
        for (std::size_t i = 0; i < size; ++i) combinations *= 3;
        for (std::size_t encoded = 0; encoded < combinations; ++encoded) {
            auto digits = encoded;
            std::vector<int> values(size);
            for (int& value : values) {
                value = static_cast<int>(digits % 3) - 1;
                digits /= 3;
            }
            test_one(values, random);
            test_merge(values, {}, random);
            test_merge({}, values, random);
            test_merge(values, values, random);
        }
    }
    for (int trial = 0; trial < 200; ++trial) {
        std::vector<int> left(random() % 41), right(random() % 41);
        for (int& value : left) value = static_cast<int>(random() % 11) - 5;
        for (int& value : right) value = static_cast<int>(random() % 11) - 5;
        test_one(left, random);
        test_merge(left, right, random);
    }
    std::cout << "Linked-list runtime checks passed: " << checks << '\n';
}
"""


def completed_source(basename):
    source = (COLLECTION / f"{basename}.cpp").read_text()
    metadata = (COLLECTION / f"{basename}.md").read_text()
    solutions = re.findall(r"^```cpp\n(.*?)^```$", metadata, re.MULTILINE | re.DOTALL)
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
    # Headers must remain outside the exercise namespace.
    includes = re.findall(r"^#include .*?$", completed, re.MULTILINE)
    completed = re.sub(r"^#include .*?\n", "", completed, flags=re.MULTILINE)
    return (
        "\n".join(includes)
        + f"\n#define HAS_{basename}\nnamespace {basename} {{\n"
        + completed
        + "}\n"
    )


def main():
    basenames = (COLLECTION / "exercise_order.md").read_text().splitlines()
    source = HARNESS + "\n".join(map(completed_source, basenames)) + CASES
    with tempfile.TemporaryDirectory(prefix="leetkatas-list-checks-") as directory:
        executable = Path(directory) / "checks"
        subprocess.run(
            shlex.split(os.environ.get("CXX", "g++"))
            + [
                "-std=c++20", "-Wall", "-Wextra", "-Werror", "-O1", "-g",
                "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                "-D_GLIBCXX_ASSERTIONS", "-x", "c++", "-", "-o", str(executable),
            ],
            input=source,
            text=True,
            check=True,
            timeout=120,
        )
        environment = os.environ.copy()
        environment["ASAN_OPTIONS"] = "detect_leaks=0"
        subprocess.run(
            [str(executable)], check=True, timeout=60, env=environment
        )


if __name__ == "__main__":
    main()
