#include <atomic>
#include <memory>
#include <string>
#include <utility>

using namespace std;

void publish(std::atomic<std::shared_ptr<const std::string>>& slot,
             std::shared_ptr<const std::string> value) {
    // Finish: transfer the shared owner into the slot so matching consumers can safely observe it
}
