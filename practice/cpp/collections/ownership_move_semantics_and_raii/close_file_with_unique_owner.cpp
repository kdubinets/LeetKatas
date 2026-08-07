#include <cstdio>
#include <memory>

struct FileCloser {
    void operator()(std::FILE* file) const {
        std::fclose(file);
    }
};

using FileOwner = std::unique_ptr<std::FILE, FileCloser>;

FileOwner solve(const char* path) {
    // Finish: open the path for reading and return an owner that closes a successfully opened file automatically
}
