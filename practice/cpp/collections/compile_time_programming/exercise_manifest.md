# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `declare_constexpr_function` | Make a pure arithmetic function usable in constant evaluation | `constexpr` function declaration |
| `construct_constexpr_value` | Make a value-type constructor usable in constant evaluation | Member-initializer list |
| `read_constexpr_member` | Make a const member operation usable in constant evaluation | `constexpr` member function |
| `sum_constexpr_array` | Evaluate a loop over fixed storage at compile time | Range-for, `std::array` |
| `sort_constexpr_array` | Sort fixed storage during constant evaluation | C++20 `std::ranges::sort` |
| `transform_constexpr_array` | Transform fixed storage during constant evaluation | C++20 `std::transform` |
| `compute_with_constexpr_vector` | Use temporary dynamic container storage during constant evaluation | C++20 constexpr `vector` |
| `inspect_constexpr_string` | Build and inspect temporary owning text during constant evaluation | C++20 constexpr `string` |
| `release_constexpr_allocation` | Release temporary dynamic storage before constant evaluation ends | C++20 constexpr `new` and `delete[]` |
| `validate_with_static_assert` | Enforce a useful computed invariant at compile time | `static_assert` |
| `declare_immediate_function` | Require every potentially evaluated call to occur at compile time | `consteval` |
| `reject_invalid_immediate_input` | Reject invalid input inside an immediate validation function | Constant-evaluation failure, `throw` |
| `invoke_immediate_lambda` | Define and call an immediately evaluated lambda | `consteval` lambda |
| `constant_initialize_storage` | Require static storage to receive constant initialization | `constinit` |
| `choose_constant_evaluation_path` | Select a constant-evaluation-safe implementation path | `is_constant_evaluated` |
| `build_constexpr_lookup_table` | Construct a computed fixed lookup table at compile time | `constexpr` loop, `std::array` |
| `run_constexpr_scope_cleanup` | Perform deterministic scope cleanup during constant evaluation | C++20 constexpr destructor |
| `dispatch_constexpr_virtual_call` | Use virtual dispatch during constant evaluation | C++20 constexpr virtual function |
