#!/usr/bin/env python3
"""Compile recorded DP solutions temporarily and compare them with simple oracles."""

import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


COLLECTION = Path(__file__).resolve().parents[1] / "collections/b_level/dynamic_programming_state_idioms"

HARNESS = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <random>
#include <string>
#include <vector>

long long checks = 0;
template<class Left, class Right>
void assert_equal(Left actual, Right expected, const char* message) {
    ++checks;
    if (actual != expected) {
        std::cerr << message << '\n';
        std::exit(1);
    }
}

long long nonadjacent_oracle(const std::vector<int>& values) {
    long long answer = 0;
    for (std::size_t mask = 0; mask < (std::size_t{1} << values.size()); ++mask) {
        if ((mask & (mask << 1)) != 0) continue;
        long long sum = 0;
        for (std::size_t i = 0; i < values.size(); ++i)
            if ((mask >> i) & 1U) sum += values[i];
        answer = std::max(answer, sum);
    }
    return answer;
}

long long knapsack_oracle(const std::vector<std::size_t>& weights,
                          const std::vector<int>& values, std::size_t capacity) {
    long long answer = 0;
    for (std::size_t mask = 0; mask < (std::size_t{1} << weights.size()); ++mask) {
        std::size_t weight = 0;
        long long value = 0;
        for (std::size_t i = 0; i < weights.size(); ++i) if ((mask >> i) & 1U) {
            weight += weights[i];
            value += values[i];
        }
        if (weight <= capacity) answer = std::max(answer, value);
    }
    return answer;
}

long long coin_oracle(const std::vector<std::size_t>& coins, std::size_t target,
                      std::size_t index = 0) {
    if (index == coins.size()) return target == 0 ? 1 : 0;
    long long result = 0;
    for (std::size_t used = 0; used <= target; used += coins[index])
        result += coin_oracle(coins, target - used, index + 1);
    return result;
}

std::size_t lcs_oracle(const std::string& left, const std::string& right) {
    std::vector<std::vector<std::size_t>> table(
        left.size() + 1, std::vector<std::size_t>(right.size() + 1));
    for (std::size_t i = 1; i <= left.size(); ++i)
        for (std::size_t j = 1; j <= right.size(); ++j)
            table[i][j] = left[i - 1] == right[j - 1]
                ? table[i - 1][j - 1] + 1
                : std::max(table[i - 1][j], table[i][j - 1]);
    return table.back().back();
}

long long cost_oracle(std::size_t index, const std::vector<int>& costs) {
    std::vector<long long> best(costs.size() + 2, 0);
    for (std::size_t i = costs.size(); i-- > index;)
        best[i] = static_cast<long long>(costs[i]) + std::min(best[i + 1], best[i + 2]);
    return index < costs.size() ? best[index] : 0;
}

void minimum_coin_search(
    const std::vector<std::size_t>& coins,
    std::size_t index,
    std::size_t remaining,
    std::size_t used,
    std::optional<std::size_t>& best) {
    if (remaining == 0) {
        if (!best || used < *best) best = used;
        return;
    }
    if (index == coins.size()) return;
    for (std::size_t count = 0; count <= remaining / coins[index]; ++count) {
        minimum_coin_search(
            coins,
            index + 1,
            remaining - count * coins[index],
            used + count,
            best);
    }
}

std::optional<std::size_t> minimum_coin_oracle(
    const std::vector<std::size_t>& coins,
    std::size_t target) {
    std::optional<std::size_t> best;
    minimum_coin_search(coins, 0, target, 0, best);
    return best;
}

void trading_search(
    const std::vector<int>& prices,
    int fee,
    std::size_t day,
    bool holding,
    long long profit,
    long long& best) {
    if (day == prices.size()) {
        if (!holding) best = std::max(best, profit);
        return;
    }
    trading_search(prices, fee, day + 1, holding, profit, best);
    if (holding) {
        trading_search(
            prices, fee, day + 1, false,
            profit + prices[day] - fee, best);
    } else {
        trading_search(
            prices, fee, day + 1, true,
            profit - prices[day], best);
    }
}

long long trading_oracle(const std::vector<int>& prices, int fee) {
    long long best = 0;
    trading_search(prices, fee, 0, false, 0, best);
    return best;
}

std::size_t lis_oracle(const std::vector<int>& values) {
    std::size_t best = 0;
    for (std::size_t mask = 0;
         mask < (std::size_t{1} << values.size());
         ++mask) {
        bool valid = true;
        bool has_prior = false;
        int prior = 0;
        std::size_t length = 0;
        for (std::size_t index = 0; index < values.size(); ++index) {
            if (((mask >> index) & 1U) == 0) continue;
            if (has_prior && values[index] <= prior) {
                valid = false;
                break;
            }
            has_prior = true;
            prior = values[index];
            ++length;
        }
        if (valid) best = std::max(best, length);
    }
    return best;
}

long long falling_path_oracle_from(
    const std::vector<std::vector<int>>& grid,
    std::size_t row,
    std::size_t column) {
    if (row + 1 == grid.size()) return grid[row][column];
    long long best = falling_path_oracle_from(grid, row + 1, column);
    if (column > 0) {
        best = std::min(
            best, falling_path_oracle_from(grid, row + 1, column - 1));
    }
    if (column + 1 < grid[row].size()) {
        best = std::min(
            best, falling_path_oracle_from(grid, row + 1, column + 1));
    }
    return static_cast<long long>(grid[row][column]) + best;
}

long long falling_path_oracle(const std::vector<std::vector<int>>& grid) {
    long long best = falling_path_oracle_from(grid, 0, 0);
    for (std::size_t column = 1; column < grid.front().size(); ++column) {
        best = std::min(best, falling_path_oracle_from(grid, 0, column));
    }
    return best;
}

int main() {
    std::mt19937 random(20260919);
    assert_equal(minimum_coin_count_with_sentinel::minimum_coin_count({2}, 3).has_value(),
          false, "unreachable coin target");
    assert_equal(*minimum_coin_count_with_sentinel::minimum_coin_count({1, 3, 4}, 6),
          std::size_t{2}, "minimum coin count");
    assert_equal(*minimum_coin_count_with_sentinel::minimum_coin_count({}, 0),
          std::size_t{0}, "zero coin target");
    assert_equal(maximum_profit_state_machine::maximum_trading_profit({1, 3, 2, 8, 4, 9}, 2),
          8LL, "coupled trading states");
    assert_equal(maximum_profit_state_machine::maximum_trading_profit({}, 4),
          0LL, "empty trading input");
    assert_equal(longest_increasing_subsequence_quadratic::longest_increasing_subsequence_length(
              {10, 9, 2, 5, 3, 7, 101, 18}),
          std::size_t{4}, "predecessor aggregation");
    assert_equal(longest_increasing_subsequence_quadratic::longest_increasing_subsequence_length(
              {2, 2, 2}),
          std::size_t{1}, "strict increasing comparison");
    assert_equal(minimum_falling_path_two_rows::minimum_falling_path_sum(
              {{2, 1, 3}, {6, 5, 4}, {7, 8, 9}}),
          13LL, "falling path rows");
    assert_equal(minimum_falling_path_two_rows::minimum_falling_path_sum({{-5}}),
          -5LL, "single falling cell");
    for (std::size_t rows = 1; rows <= 9; ++rows) {
        for (std::size_t columns = 1; columns <= 9; ++columns) {
            std::vector<std::vector<long long>> ways(rows, std::vector<long long>(columns, 1));
            for (std::size_t i = 1; i < rows; ++i)
                for (std::size_t j = 1; j < columns; ++j)
                    ways[i][j] = ways[i - 1][j] + ways[i][j - 1];
            assert_equal(count_grid_paths_rolling_row::count_grid_paths(rows, columns),
                  ways.back().back(), "grid paths");
        }
    }
    for (unsigned mask = 0; mask < 64; ++mask) {
        std::vector<std::size_t> coins;
        for (std::size_t coin = 1; coin <= 6; ++coin)
            if ((mask >> (coin - 1)) & 1U) coins.push_back(coin);
        for (std::size_t target = 0; target <= 18; ++target) {
            assert_equal(count_unordered_coin_combinations::count_coin_combinations(coins, target),
                  coin_oracle(coins, target), "coin combinations");
            assert_equal(minimum_coin_count_with_sentinel::minimum_coin_count(coins, target),
                  minimum_coin_oracle(coins, target), "minimum coin count");
        }
    }
    for (int trial = 0; trial < 3000; ++trial) {
        const std::size_t size = random() % 11;
        std::vector<int> values(size), costs(size);
        std::vector<std::size_t> weights(size);
        for (std::size_t i = 0; i < size; ++i) {
            values[i] = static_cast<int>(random() % 15) - 5;
            costs[i] = static_cast<int>(random() % 21) - 10;
            weights[i] = random() % 7 + 1;
        }
        assert_equal(maximum_nonadjacent_sum_rolling::maximum_nonadjacent_sum(values),
              nonadjacent_oracle(values), "nonadjacent sum");
        std::vector<int> nonnegative = values;
        for (int& value : nonnegative) value = std::max(value, 0);
        const std::size_t capacity = random() % 20;
        assert_equal(maximum_zero_one_capacity_value::maximum_capacity_value(
                  weights, nonnegative, capacity),
              knapsack_oracle(weights, nonnegative, capacity), "zero-one capacity");
        assert_equal(longest_increasing_subsequence_quadratic::longest_increasing_subsequence_length(
                  values),
              lis_oracle(values), "longest increasing subsequence");
        for (std::size_t start = 0; start <= size + 2; ++start) {
            assert_equal(minimum_step_cost_memoized::minimum_step_cost_from(start, costs),
                  cost_oracle(start, costs), "memoized cost");
        }
        std::string left(random() % 9, 'a'), right(random() % 9, 'a');
        for (char& value : left) value = static_cast<char>('a' + random() % 4);
        for (char& value : right) value = static_cast<char>('a' + random() % 4);
        assert_equal(longest_common_subsequence_rolling::longest_common_subsequence_length(left, right),
              lcs_oracle(left, right), "longest common subsequence");
    }
    assert_equal(minimum_step_cost_memoized::minimum_step_cost_from(0, std::vector<int>(100, 0)),
          0LL, "memoized zero-cost chain");
    for (int trial = 0; trial < 2000; ++trial) {
        std::vector<int> prices(random() % 10);
        for (int& price : prices) price = static_cast<int>(random() % 21);
        const int fee = static_cast<int>(random() % 8);
        assert_equal(maximum_profit_state_machine::maximum_trading_profit(prices, fee),
              trading_oracle(prices, fee), "trading state machine");

        const std::size_t rows = random() % 5 + 1;
        const std::size_t columns = random() % 5 + 1;
        std::vector<std::vector<int>> grid(rows, std::vector<int>(columns));
        for (auto& row : grid) {
            for (int& value : row) {
                value = static_cast<int>(random() % 21) - 10;
            }
        }
        assert_equal(minimum_falling_path_two_rows::minimum_falling_path_sum(grid),
              falling_path_oracle(grid), "falling path rows");
    }
    std::cout << "Dynamic-programming runtime checks passed: " << checks << '\n';
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
        lambda match: "\n".join(match[1] + line for line in solutions[0].rstrip().splitlines()),
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
    with tempfile.TemporaryDirectory(prefix="leetkatas-dp-checks-") as directory:
        executable = Path(directory) / "checks"
        subprocess.run(
            shlex.split(os.environ.get("CXX", "g++")) + [
                "-std=c++20", "-Wall", "-Wextra", "-Werror", "-O1", "-g",
                "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                "-D_GLIBCXX_ASSERTIONS", "-x", "c++", "-", "-o", str(executable),
            ], input=source, text=True, check=True, timeout=120,
        )
        environment = os.environ.copy()
        environment["ASAN_OPTIONS"] = "detect_leaks=0"
        subprocess.run([str(executable)], check=True, timeout=60, env=environment)


if __name__ == "__main__":
    main()
