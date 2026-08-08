#include <filesystem>
#include <system_error>

void solve(
    const std::filesystem::path& value,
    std::filesystem::file_time_type time,
    std::error_code& error) {
    // Finish: set the entry's modification time while placing failure in error
}
