#include <filesystem>
#include <system_error>
#include <vector>

std::vector<std::filesystem::path> solve(
    const std::filesystem::path& directory,
    std::error_code& error) {
    // Finish: collect direct child paths while reporting construction or increment failure in error
}
