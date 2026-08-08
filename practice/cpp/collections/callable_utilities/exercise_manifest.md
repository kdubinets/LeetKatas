# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `make_erased_multiplier` | Store a capturing lambda behind a fixed callable signature | `std::function`, value capture |
| `select_overloaded_function` | Resolve an overloaded function name to a stored callable signature | Function-pointer cast, `std::function` |
| `invoke_callback_if_present` | Test and invoke a possibly empty type-erased callback | Nullable callable state |
| `clear_stored_callback` | Reset a type-erased callback to its empty state | `std::function` assignment |
| `run_callbacks_in_order` | Invoke a sequence of stored callbacks in iteration order | Vector of `std::function` |
| `make_stateful_counter` | Preserve mutable lambda state inside a type-erased callable | Initialized capture, repeated calls |
| `invoke_member_function` | Uniformly invoke a pointer-to-member function on an object | `std::invoke` |
| `invoke_member_data` | Uniformly access member data through a member pointer | `std::invoke`, reference result |
| `forward_callable_invocation` | Preserve argument and result value categories through generic invocation | `std::invoke`, perfect forwarding |
| `bind_leading_value` | Create a unary callable by binding a leading value | `std::bind_front` |
| `bind_member_to_reference` | Bind a member function to an existing object without copying it | `std::bind_front`, `std::ref` |
| `collect_mutable_references` | Build a container of mutable aliases to existing elements | `reference_wrapper`, vector lifetime |
| `rebind_reference_wrapper` | Redirect a reference wrapper to a different object | Assignment semantics |
| `wrap_const_reference` | Create a copyable wrapper around a const object reference | `std::cref` |
| `adapt_member_function` | Turn a member-function pointer into an ordinary callable object | `std::mem_fn` |
| `negate_stored_predicate` | Adapt a predicate to return its logical complement | `std::not_fn` |
| `make_generic_size_callable` | Define one lambda call operator for multiple size-bearing types | Generic lambda parameter |
| `make_same_type_pair_callable` | Use an explicit lambda template list to couple parameter types | C++20 template lambda |
| `capture_unique_owner` | Transfer move-only state into a returned callable | Initialized capture, ownership |
| `apply_noncopyable_callable_by_reference` | Pass a non-copyable stateful callable through a copying algorithm interface | `std::ref`, ranges algorithm |
