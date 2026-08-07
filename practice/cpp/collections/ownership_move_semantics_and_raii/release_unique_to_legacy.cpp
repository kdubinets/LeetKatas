#include <memory>

struct Resource {
    int id;
};

void legacy_adopt(Resource* resource);

void solve(std::unique_ptr<Resource>& owner) {
    // Finish: give the owned resource to the legacy function that assumes responsibility for destroying it
}
