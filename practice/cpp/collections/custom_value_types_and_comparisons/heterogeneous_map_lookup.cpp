#include <map>
#include <optional>

struct Ticket {
    int number;
};

struct TicketOrder {
    using is_transparent = void;
    bool operator()(Ticket left, Ticket right) const { return left.number < right.number; }
    bool operator()(Ticket left, int right) const { return left.number < right; }
    bool operator()(int left, Ticket right) const { return left < right.number; }
};

std::optional<double> solve(const std::map<Ticket, double, TicketOrder>& prices, int number) {
    // Finish: return the price for the numeric key without constructing a custom key
}
