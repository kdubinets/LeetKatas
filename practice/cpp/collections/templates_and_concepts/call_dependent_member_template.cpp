struct Reader {
    template <class T>
    T read() const {
        return T{7};
    }
};

template <class Source>
int read_integer(const Source& source) {
    // Finish: ask the source for an int through its dependent read member
}

int main() {
    return read_integer(Reader{}) == 7 ? 0 : 1;
}
