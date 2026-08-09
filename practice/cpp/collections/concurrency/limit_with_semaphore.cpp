#include <semaphore>

void run_with_permit(std::counting_semaphore<>& permits,
                     void (*work)() noexcept) {
    // Finish: reserve one permit, run the non-throwing work, and return the permit
}
