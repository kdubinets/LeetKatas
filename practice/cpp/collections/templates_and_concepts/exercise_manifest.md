# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `define_function_template` | Generalize one function over a deduced value type | Template type parameter |
| `define_two_type_template` | Deduce independent types for two function parameters | Multiple template parameters |
| `specify_template_argument` | Supply an explicit template argument at a call site | Conversion, function template call |
| `define_nontype_array_template` | Deduce an array bound as a non-type template argument | Array reference, `std::size_t` |
| `define_class_template` | Parameterize a small value holder by its stored type | Class template, member initialization |
| `define_alias_template` | Parameterize a type alias by its element type | Alias template, `std::vector` |
| `define_variable_template` | Define a type-dependent compile-time variable | Variable template, type trait |
| `default_template_type_argument` | Supply a default type argument while preserving explicit selection | Alias template, class template |
| `add_class_deduction_guide` | Deduce class template arguments from a constructor-shaped call | User-defined deduction guide |
| `specialize_type_mapping` | Fully specialize a type mapping for one source type | Explicit specialization |
| `partially_specialize_pointer_trait` | Recognize every pointer type with a partial specialization | Trait inheritance, pointer pattern |
| `define_member_function_template` | Parameterize a member operation independently of its enclosing class | Explicit and deduced function-template arguments |
| `use_dependent_type_name` | Identify a dependent nested name as a type | Alias template, nested `value_type` |
| `call_dependent_member_template` | Identify a dependent member name as a template before calling it | Explicit template argument, member access |
| `count_template_arguments` | Compute the size of a template argument pack | `sizeof...` |
| `construct_from_argument_pack` | Expand forwarded arguments into object construction | Parameter pack, emplacement |
| `call_for_each_argument` | Expand one operation over every function argument | Comma fold, forwarding |
| `sum_argument_pack` | Combine all arguments with a supplied initial value | Binary fold, empty pack |
| `check_all_same_type` | Fold a type predicate across a parameter pack | `is_same_v`, conjunction fold |
| `select_type_with_conditional` | Choose one of two types from a compile-time condition | `conditional_t` |
| `normalize_deduced_type` | Remove references and cv-qualifiers from a type | `remove_cvref_t` |
| `deduce_common_value_type` | Select a common conversion type for a type pack | `common_type_t`, alias template |
| `branch_on_type_category` | Compile only the branch valid for a type category | `if constexpr`, integral trait |
| `detect_size_member` | Detect whether a type supports a size member expression | `void_t`, partial specialization |
| `enable_integral_overload` | Restrict a function template through its return type | `enable_if_t`, integral trait |
| `define_integral_concept` | Name an integral-type requirement | Concept definition, standard concept |
| `constrain_template_parameter` | Constrain a template parameter directly | Type-constraint syntax |
| `write_abbreviated_template` | Constrain an inferred function parameter | Abbreviated function template |
| `require_member_expression` | Accept types that provide a callable member expression | Requires-expression, expression requirement |
| `require_exact_result_type` | Require an expression to produce one exact type | Compound requirement, `same_as` |
| `require_convertible_result` | Require an expression result to convert to a target type | Compound requirement, `convertible_to` |
| `require_noexcept_expression` | Require an operation to be non-throwing | Compound requirement, `noexcept` |
| `require_nested_type` | Accept types that declare a specified nested type | Type requirement |
| `require_compile_time_condition` | Enforce a Boolean relationship between type properties | Nested requirement, `sizeof` |
| `constrain_with_requires_clause` | Express a relationship between multiple deduced types | Trailing requires-clause |
| `prefer_refined_concept_overload` | Select a more constrained overload for a refined concept | Concept refinement, subsumption |
