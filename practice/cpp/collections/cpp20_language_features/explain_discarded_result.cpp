struct Status {
    bool ok;
};

// Finish: require callers to inspect this result and diagnose discards with "check the status"
Status check_status(bool ok) {
    return {ok};
}

int main() {
    return check_status(true).ok ? 0 : 1;
}
