# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `consume_decimal_integer` | Parse a decimal integer prefix and advance a string view | `from_chars`, non-owning input |
| `parse_hexadecimal_integer` | Parse a complete hexadecimal integer | `from_chars`, explicit base |
| `parse_floating_point_value` | Parse a complete floating-point value | `from_chars`, general format |
| `classify_integer_parse` | Distinguish invalid, out-of-range, trailing, and successful integer input | `from_chars`, `std::errc` |
| `convert_integer_to_decimal` | Convert an integer to decimal text without a stream | `to_chars`, bounded local buffer |
| `convert_integer_to_hexadecimal` | Convert an unsigned integer to hexadecimal text | `to_chars`, explicit base |
| `convert_fixed_precision_value` | Convert a floating-point value with fixed precision | `to_chars`, `chars_format` |
| `write_integer_to_buffer` | Write integer text into caller-provided storage when it fits | `to_chars`, `std::span`, capacity failure |
| `extract_word_and_count` | Extract typed whitespace-delimited fields from text | Input string stream, optional result |
| `parse_textual_boolean` | Extract a textual Boolean value | `boolalpha`, stream validation |
| `parse_hexadecimal_stream` | Extract an integer using hexadecimal stream state | Input manipulator |
| `format_fixed_decimal_stream` | Format a floating-point value with fixed precision in a stream | Output manipulators |
| `format_padded_number_stream` | Format a number with width and fill | `setw`, `setfill` |
| `quote_text_for_stream` | Escape and delimit text for stream transport | `std::quoted`, output stream |
| `extract_quoted_text` | Extract one escaped quoted value from text | `std::quoted`, input stream |
| `compile_case_insensitive_regex` | Compile a reusable case-insensitive pattern and translate syntax failure | `regex_error`, syntax options |
| `check_full_regex_match` | Test whether a pattern matches the complete input | `regex_match`, precompiled pattern |
| `find_first_regex_match` | Locate the first pattern match and report its bounds | `regex_search`, match results |
| `extract_regex_capture` | Safely extract one capture from the first match | `smatch`, unmatched groups, bounds |
| `collect_all_regex_matches` | Iterate over every non-overlapping pattern match | `sregex_iterator`, result collection |
| `split_on_regex_matches` | Collect unmatched fields separated by pattern matches | `sregex_token_iterator`, submatch index `-1` |
| `replace_all_regex_matches` | Replace every non-overlapping pattern match | `regex_replace`, replacement text |
| `replace_first_regex_match` | Restrict regular-expression replacement to the first match | `regex_replace`, format flags |
| `format_named_measurement` | Construct structured text with a compile-time format string | `std::format`, precision |
| `format_centered_label` | Center text in a filled field | `std::format`, dynamic width |
| `append_formatted_text` | Append formatted fields directly to existing text | `format_to`, output iterator |
| `format_to_bounded_buffer` | Write bounded formatted output and report truncation sizes | `format_to_n`, caller-owned storage |
| `format_with_runtime_pattern` | Apply a runtime-selected format pattern | `std::vformat`, format arguments |
