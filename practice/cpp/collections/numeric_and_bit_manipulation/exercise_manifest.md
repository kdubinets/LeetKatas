# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `check_single_bit` | Test whether an unsigned value has exactly one set bit | `has_single_bit` |
| `measure_bit_width` | Measure the bits needed to represent an unsigned value | `bit_width`, zero behavior |
| `count_leading_zero_bits` | Count zero bits before the most-significant set bit | `countl_zero`, zero behavior |
| `count_trailing_zero_bits` | Count zero bits after the least-significant set bit | `countr_zero`, zero behavior |
| `round_down_power_of_two` | Find the greatest power of two not exceeding a value | `bit_floor` |
| `round_up_power_of_two` | Find the least power of two not less than a value | `bit_ceil`, representable precondition |
| `rotate_bits_left` | Circularly rotate an unsigned value | `rotl`, normalized distance |
| `bit_cast_object_representation` | Copy a value's object representation into bytes | `bit_cast`, byte array |
| `make_low_bits_mask` | Construct a mask containing a requested number of low one bits | Unsigned digits, full-width case |
| `enable_bit_flag` | Set one indexed flag without changing other bits | Unsigned shift, bitwise OR |
| `disable_bit_flag` | Clear one indexed flag without changing other bits | Unsigned mask, bitwise AND |
| `check_bit_flag` | Test one indexed flag without mutation | Unsigned mask, bitwise AND |
| `toggle_bit_flag` | Reverse one indexed flag without changing other bits | Unsigned mask, bitwise XOR |
| `extract_bit_field` | Extract a fixed-width field from an unsigned value | Shift and mask |
| `replace_bit_field` | Replace a fixed-width field while preserving other bits | Clear mask, bounded insertion |
| `set_bitset_positions` | Set listed positions in a fixed-size bitset | Bounds precondition, indexed mutation |
| `shift_bitset_window` | Shift a fixed-size bitset toward higher positions | `bitset` compound shift |
| `check_integer_representable` | Test whether an integer value fits a destination type | `in_range`, safe conversion |
| `compare_signed_and_unsigned` | Compare signed and unsigned integers safely | `cmp_less` |
| `interpolate_numeric_value` | Interpolate between floating-point endpoints | `lerp` |
| `round_to_long_integer` | Round halfway cases away from zero into a long integer | `lround` |
| `reduce_integer_product` | Reduce a range to a widened product | `reduce`, identity type |
| `sum_squared_values` | Transform and reduce a range in one operation | `transform_reduce`, widened arithmetic |
| `generate_uniform_integers` | Generate values from an inclusive uniform integer interval | `mt19937`, distribution state |
| `shuffle_with_seed` | Reorder a sequence reproducibly from a seed | `shuffle`, engine construction |
| `sample_values_with_seed` | Select a bounded random sample without replacement | `sample`, output iterator, seeded engine |
