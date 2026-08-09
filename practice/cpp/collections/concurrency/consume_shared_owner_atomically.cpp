#include <atomic>
#include <memory>
#include <string>

std::shared_ptr<const std::string> consume(
    const std::atomic<std::shared_ptr<const std::string>>& slot) {
    // Finish: return a shared owner that safely observes the published immutable string
}
