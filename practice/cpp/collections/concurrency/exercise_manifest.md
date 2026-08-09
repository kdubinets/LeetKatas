# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `join_thread_before_read` | Join a worker before reading the state it produced | `std::thread`, happens-before |
| `pass_reference_to_thread` | Pass caller-owned state by reference through thread argument decay | `std::ref`, join |
| `transfer_owner_to_thread` | Transfer move-only ownership into a worker thread | `std::move`, `unique_ptr` |
| `rely_on_jthread_join` | Use scoped thread lifetime to complete work before returning | `std::jthread`, automatic join |
| `observe_stop_request` | Check a cooperative cancellation request through a stop token | `stop_requested` |
| `request_jthread_stop` | Request cancellation from a jthread's associated stop source | Deterministic gate, join |
| `run_stop_callback` | Register work that runs synchronously when stop is requested | `stop_callback`, `stop_source` |
| `protect_value_with_lock_guard` | Hold a mutex for one complete scoped mutation | `lock_guard` |
| `defer_unique_lock` | Construct an unlocked movable lock and acquire it later | `unique_lock`, `defer_lock` |
| `unlock_before_slow_work` | Release a movable lock before operating on an independent protected-state snapshot | `unique_lock`, reduced critical section |
| `lock_two_mutexes` | Acquire two mutexes together without lock-order deadlock | `scoped_lock` |
| `wait_for_condition` | Wait on a condition variable with a state predicate | `unique_lock`, spurious wakeups |
| `publish_condition_change` | Change guarded state before notifying one waiter | `lock_guard`, `notify_one` |
| `wait_with_stop_token` | Perform a cancellable predicate wait | `condition_variable_any`, `stop_token` |
| `increment_atomic_counter` | Increment an atomic counter and return its previous value | `fetch_add` |
| `increment_relaxed_statistic` | Update an independent atomic statistic without ordering unrelated memory | `memory_order_relaxed`, `fetch_add` |
| `exchange_atomic_state` | Atomically replace a value and retrieve the old state | `atomic::exchange` |
| `compare_exchange_atomic_value` | Attempt a conditional atomic replacement while preserving observed failure state | `compare_exchange_strong`, expected parameter |
| `increment_through_atomic_ref` | Apply atomic access to caller-owned non-atomic storage | `atomic_ref` |
| `publish_with_release` | Publish ordinary state with a release store | Memory ordering |
| `consume_with_acquire` | Observe publication with an acquire load before reading payload | Memory ordering |
| `wait_for_atomic_change` | Block until an atomic value differs from an observed state | C++20 `atomic::wait` |
| `notify_atomic_waiters` | Store a new atomic state and wake all waiters | C++20 `atomic::notify_all` |
| `synchronize_with_latch` | Arrive at a one-shot synchronization point and wait for all participants | `latch::arrive_and_wait` |
| `synchronize_barrier_phase` | Split arrival at a reusable phase boundary from waiting for completion | `barrier::arrival_token`, independent work |
| `limit_with_semaphore` | Acquire and release one permit around non-throwing work | `counting_semaphore` |
| `fulfill_promise` | Create a future and make a value available through its promise | `promise`, `future` |
| `consume_future_result` | Consume the single value from a future | Blocking retrieval, move-only handle |
| `propagate_promise_exception` | Store the active exception in a promise | `current_exception`, future propagation |
| `launch_async_task` | Launch a callable asynchronously with an explicit policy | `std::async`, `launch::async` |
| `execute_packaged_task` | Connect a packaged callable to its future and run it on a thread | `packaged_task`, ownership transfer |
| `read_with_shared_lock` | Protect read-only access with shared ownership of a mutex | `shared_mutex`, `shared_lock` |
| `write_with_exclusive_lock` | Protect mutation with exclusive ownership of a shared mutex | `shared_mutex`, `unique_lock` |
| `initialize_once` | Run an initialization callable once for a supplied flag | `call_once`, perfect forwarding |
| `publish_shared_owner_atomically` | Publish shared ownership through an atomic smart pointer | `atomic<shared_ptr<T>>`, release store |
| `consume_shared_owner_atomically` | Acquire shared ownership from an atomic smart pointer | `atomic<shared_ptr<T>>`, acquire load |
| `write_synchronized_record` | Emit one complete stream record without interleaving between threads | `osyncstream`, scope-based emission |
