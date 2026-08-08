#include <set>
#include <string>
#include <string_view>

struct Name {
    std::string value;
};

struct NameOrder {
    using is_transparent = void;
    bool operator()(const Name& left, const Name& right) const { return left.value < right.value; }
    bool operator()(const Name& left, std::string_view right) const { return left.value < right; }
    bool operator()(std::string_view left, const Name& right) const { return left < right.value; }
};

bool solve(const std::set<Name, NameOrder>& names, std::string_view target) {
    // Finish: return whether the target is present without constructing an owning key
}
