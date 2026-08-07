#include <memory>

struct Resource {
    int id;
};

Resource* legacy_create(int id);

std::unique_ptr<Resource> solve(int id) {
    // Finish: immediately place the newly allocated legacy result under exclusive ownership
}
