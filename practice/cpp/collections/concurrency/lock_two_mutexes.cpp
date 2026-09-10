#include <mutex>
#include <utility>

using namespace std;

void swap_values(int& first, std::mutex& first_mutex,
                 int& second, std::mutex& second_mutex) {
    // Finish: acquire both mutexes together and exchange the protected values
}
