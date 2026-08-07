#include <memory>

struct Resource {
    int id;
};

Resource* acquire_resource(int id);
void release_resource(Resource* resource, int channel) noexcept;

struct ResourceDeleter {
    int channel;

    void operator()(Resource* resource) const noexcept {
        release_resource(resource, channel);
    }
};

using ResourceOwner = std::unique_ptr<Resource, ResourceDeleter>;

ResourceOwner solve(int id, int release_channel) {
    // Finish: acquire the resource and bind it to a deleter configured with the release channel
}
