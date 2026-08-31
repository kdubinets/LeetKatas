#include <cstddef>
#include <functional>
#include <string>
#include <string_view>
#include <unordered_set>

// Finish: define matching policies that let owning strings be found with string views without allocation and give equal text representations identical hashes

using Names = std::unordered_set<std::string, NameHash, NameEqual>;
