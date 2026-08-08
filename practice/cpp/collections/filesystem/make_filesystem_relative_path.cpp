#include <filesystem>
#include <system_error>

std::filesystem::path solve(
    const std::filesystem::path& value,
    const std::filesystem::path& base,
    std::error_code& error) {
    // Finish: resolve value relative to base while reporting filesystem failures in error
}
