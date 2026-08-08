#include <filesystem>
#include <system_error>

void solve(
    const std::filesystem::path& value,
    std::filesystem::perms additions,
    std::error_code& error) {
    // Finish: add the requested permission bits without replacing existing bits or throwing
}
