constexpr bool valid_port(int value) {
    return value > 0 && value <= 65535;
}

// Finish: require at compile time that port 443 satisfies the supplied validity rule
