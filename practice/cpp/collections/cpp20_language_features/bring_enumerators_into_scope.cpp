enum class Status {
    idle,
    running,
    stopped
};

bool is_active(Status status) {
    // Finish: import the status names and compare against running without qualification
}

int main() {
    return is_active(Status::running) && !is_active(Status::idle) ? 0 : 1;
}
