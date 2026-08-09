#include <cstddef>
#include <functional>
#include <memory>
#include <string>
#include <thread>

void consume(std::unique_ptr<std::string> text, std::size_t& length) {
    length = text->size();
}

std::size_t solve(std::unique_ptr<std::string> text) {
    std::size_t length = 0;
    // Finish: give the string owner to a worker, collect its length, and wait for completion
}
