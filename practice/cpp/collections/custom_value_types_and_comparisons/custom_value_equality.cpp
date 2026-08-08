#include <string>

struct Account {
    int id;
    std::string display_name;
    int cached_score;

    friend bool operator==(const Account& left, const Account& right) {
        // Finish: compare accounts by stable identity and display name while ignoring cached data
    }
};
