#include <cstdint>
#include <filesystem>
#include <system_error>
#include <variant>

using Result = std::variant<std::uintmax_t, std::error_code>;

Result solve(const std::filesystem::path& path) {
    // Finish: return the file size or the non-throwing operation's error
}
