# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `construct_variant_alternative` | Construct a variant in a selected alternative | In-place type tag, duplicate-convertibility avoidance |
| `check_variant_alternative` | Test which type a variant currently contains | Safe state inspection |
| `read_variant_if_type` | Read an alternative without throwing when its type is active | Pointer-style access, optional result |
| `replace_variant_alternative` | Replace a variant value by constructing another alternative in place | Emplacement, returned reference |
| `visit_variant_to_text` | Convert every variant alternative to one common result type | Generic visitor, `if constexpr` |
| `visit_variant_with_overloads` | Handle variant alternatives with an overload set | Visitor composition, distinct behavior |
| `mutate_variant_value` | Mutate the active alternative through visitation | Generic reference parameter |
| `combine_two_variants` | Visit two variants simultaneously | Multi-variant dispatch |
| `handle_empty_variant_state` | Represent and identify an explicit empty variant state | `monostate` |
| `transform_optional_value` | Transform a present optional while preserving absence | Manual C++20 composition |
| `chain_optional_operation` | Continue with an optional-producing operation only when input exists | Flattened optional result |
| `combine_optional_values` | Produce a value only when two optionals are present | Absence propagation |
| `convert_optional_to_result` | Convert absence into a specific explicit error | Ownership transfer, value-or-error model |
| `transform_result_value` | Map the success value while preserving an explicit error | Result propagation |
| `chain_result_operation` | Continue with a result-producing operation only after success | Flat result, short-circuit propagation |
| `transform_result_error` | Map an explicit error while preserving a success | Error adaptation |
| `combine_result_values` | Combine two successful results or propagate the first error | Deterministic error precedence |
| `translate_exception_to_result` | Convert a throwing operation into an explicit success-or-error value | Exception boundary |
| `rethrow_with_nested_context` | Add contextual failure information while preserving the original exception | Nested exceptions |
| `read_file_size_error_code` | Use a non-throwing filesystem operation and propagate its error code | Output error parameter |
| `throw_reported_error` | Convert a reported error code into an exception with context | `system_error`, output error parameter |
