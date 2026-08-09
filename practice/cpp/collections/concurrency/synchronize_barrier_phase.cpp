#include <barrier>
#include <utility>

void finish_phase(std::barrier<>& phase,
                  void (*independent_work)() noexcept) {
    // Finish: record this participant's arrival, perform the independent work, and then wait for the phase to complete
}
