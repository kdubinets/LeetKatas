# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `read_complete_line` | Read one complete line from a supplied input stream | `std::getline`, optional result |
| `read_delimited_field` | Read through a caller-selected delimiter while preserving empty fields | Three-argument `std::getline` |
| `read_count_and_next_line` | Transition from formatted numeric extraction to the following complete line | Remainder discard, mixed input modes |
| `collect_lines_until_eof` | Collect complete lines while distinguishing normal EOF from another stream failure | Stream-state inspection |
| `recover_after_invalid_line` | Clear failed formatted input and discard the rest of its record before retrying | `clear`, `ignore` |
| `write_key_value_record` | Write one specified textual record through a caller-provided stream | Stream insertion, output-state result |
| `open_text_file_for_reading` | Open a C++ input file and represent open failure explicitly | `ifstream`, move-only optional value |
| `open_text_file_for_appending` | Open a C++ output file without replacing existing contents | `ofstream`, append mode |
| `open_text_file_for_replacement` | Open a C++ output file while explicitly replacing existing contents | `ofstream`, truncation mode |
| `open_binary_file_at_end` | Open a binary input file initially positioned at its end | Combined open modes |
| `seek_input_position` | Reposition a seekable input stream to a supplied absolute stream position | State reset, `seekg`, `tellg` |
| `query_input_end_position` | Query the opaque end position of a seekable input stream | `seekg`, `tellg`, optional position |
| `rewind_input_stream` | Recover a possibly exhausted input stream and return it to the beginning | `clear`, absolute seek |
| `patch_output_position` | Reposition a seekable output stream and replace one character | `seekp`, `put`, stream-state result |
| `read_exact_bytes` | Fill a bounded byte destination and report whether every requested byte was read | Unformatted read, `gcount` |
| `write_exact_bytes` | Write a bounded byte source and report whether the stream accepted it | Unformatted write, output state |
| `copy_stream_contents` | Transfer remaining characters through stream-buffer iterators and detect output failure | Empty-input success, caller-owned streams |
| `view_output_stream_buffer` | Borrow accumulated output text without copying or transferring its buffer | C++20 string-stream `view`, lifetime boundary |
| `move_text_into_input_stream` | Install owned text as a C++20 input string-stream buffer without copying it | Rvalue `str` setter |
| `move_text_out_of_output_stream` | Extract an output string-stream buffer as an owned string without copying it | Rvalue-qualified `str` getter |
