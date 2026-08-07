# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `make_unique_record` | Construct one exclusively owned object | `make_unique`, constructor arguments |
| `clone_unique_record` | Deep-copy a nullable exclusively owned object | Independent allocation, const source |
| `make_unique_array` | Construct a value-initialized exclusively owned array | Runtime extent |
| `transfer_unique_owner` | Move-assign exclusive ownership | Empty moved-from pointer |
| `store_unique_owner` | Move one exclusive owner into a container | Move-only element |
| `replace_unique_resource` | Replace exclusive ownership with a new object | Automatic old-resource cleanup |
| `destroy_unique_resource` | Release an exclusively owned object immediately | `reset` |
| `release_unique_to_legacy` | Relinquish ownership to an adopting legacy API | `release` boundary |
| `adopt_legacy_resource` | Adopt a raw owning result immediately | Explicit unique ownership |
| `observe_unique_resource` | Obtain a non-owning pointer from an exclusive owner | `get`, nullable observer |
| `wrap_resource_with_deleter` | Bind a resource to its custom release operation | Stateful unique-pointer type |
| `upcast_unique_owner` | Convert exclusive ownership to a polymorphic base | Converting move, virtual destructor |
| `make_shared_record` | Construct a shared object in one allocation | `make_shared` |
| `store_shared_owner` | Copy shared ownership into a container | Reference count extension |
| `promote_unique_to_shared` | Transfer exclusive ownership into shared ownership | Converting constructor |
| `downcast_shared_owner` | Check and convert polymorphic shared ownership | Shared control block, failed cast |
| `lock_weak_observer` | Acquire temporary shared ownership when still alive | `weak_ptr::lock` |
| `check_weak_expiration` | Observe whether all owners are gone | Non-owning state query |
| `assign_weak_back_link` | Create a non-owning graph back-link | Cycle avoidance |
| `alias_shared_member` | Share owner lifetime while pointing at a member | Aliasing constructor |
| `obtain_shared_self` | Acquire shared ownership of the current object | `enable_shared_from_this`, one control block |
| `drop_shared_owner` | Relinquish one shared ownership stake | Other owners remain valid |
| `move_string_into_optional` | Move a string into optional storage | Source remains valid |
| `move_member_out` | Move an owned member into a return value | Explicit member transfer |
| `move_vector_into_member` | Move-assign a container into object storage | Ownership of allocation |
| `return_local_by_implicit_move` | Return a by-value parameter without redundant `std::move` | Implicit move, elision freedom |
| `verify_unique_source_after_move` | Observe the defined empty state of a moved-from unique pointer | Ownership transfer invariant |
| `reuse_moved_from_string` | Assign a new value to a valid moved-from string | Unspecified contents, valid state |
| `exchange_unique_owner` | Atomically take ownership and leave null | `std::exchange`, move-only value |
| `declare_move_only_owner` | Express movable but non-copyable special members | Defaulted moves, deleted copies |
| `store_rule_of_zero_buffer` | Choose an owning member that supplies value semantics | Rule of zero, vector storage |
| `move_construct_handle` | Transfer a scalar handle during move construction | Source invalidation |
| `move_assign_handle` | Release then transfer a scalar handle during move assignment | Self-assignment safety |
| `release_handle_in_destructor` | Release a valid non-memory handle at scope exit | Custom RAII destructor |
| `close_file_with_unique_owner` | Manage a C file handle with a custom deleter | `fclose`, null safety |
| `restore_flag_with_scope_guard` | Install a guard before running an operation | Cleanup on normal and exceptional exit |
