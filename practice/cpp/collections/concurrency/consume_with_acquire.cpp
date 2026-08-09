#include <atomic>
#include <optional>

std::optional<int> try_consume(const int& payload,
                               const std::atomic<bool>& ready) {
    // Finish: return no value unless publication is observed with ordering that makes the payload safe to read
}
