#include <cstddef>
#include <string>
#include <variant>

template<class... Fs>
struct Overloaded : Fs... { using Fs::operator()...; };
template<class... Fs>
Overloaded(Fs...) -> Overloaded<Fs...>;

std::size_t solve(const std::variant<int, std::string>& value) {
    // Finish: return an integer's magnitude as a size or a string's length
}
