# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `initialize_aggregate_by_member` | Initialize selected aggregate members by name | Designated initializers, declaration order |
| `default_unspecified_aggregate_members` | Designate one aggregate member while retaining defaults for the others | Default member initializers, designated initializer |
| `initialize_nested_aggregate_members` | Designate an aggregate-valued member with an inner initializer | Nested aggregate initialization |
| `parenthesize_aggregate_initialization` | Direct-initialize an aggregate through parentheses | C++20 parenthesized aggregate initialization |
| `retain_range_owner_during_iteration` | Keep a temporary range owner alive through a range-for initializer | Range-for init-statement, lifetime |
| `bring_enumerators_into_scope` | Import scoped enumerator names for unqualified use | `using enum` |
| `make_conversion_conditionally_explicit` | Make a converting constructor explicit only for selected source types | Conditional `explicit`, type trait |
| `capture_argument_pack_by_value` | Init-capture every argument from a parameter pack | Pack expansion in lambda capture |
| `default_construct_captureless_lambda` | Construct another object of a captureless lambda's closure type | C++20 defaulted closure constructor |
| `use_lambda_type_in_unevaluated_context` | Embed a directly written lambda's closure type in another type | `decltype`, default-constructible captureless closure |
| `store_utf8_code_units` | Use the distinct UTF-8 character type for a UTF-8 literal | `char8_t`, `u8string_view` |
| `allow_empty_member_overlap` | Mark an empty data member as potentially address-sharing | `no_unique_address` attribute |
| `mark_unlikely_empty_branch` | Mark an uncommon branch for optimization guidance | `unlikely` attribute, early return |
| `explain_discarded_result` | Attach an explanatory diagnostic to a result that should be inspected | Reason-bearing `nodiscard` attribute |
| `add_optional_variadic_comma` | Emit a comma only when variadic macro arguments are present | `__VA_OPT__`, variadic macro |
