# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `join_path_components` | Join path components with platform-aware separator handling | Non-mutating path construction |
| `extract_path_filename` | Extract the final filename component from a path | Lexical path query |
| `extract_stem_and_extension` | Decompose a filename into stem and extension paths | Multi-part lexical query |
| `extract_parent_path` | Obtain every path component before the filename | Lexical path query |
| `replace_path_filename` | Replace a path's final filename on a value copy | Path mutation |
| `replace_path_extension` | Replace a path's final extension on a value copy | Path mutation |
| `append_filename_suffix` | Concatenate a suffix without inserting a path separator | Path concatenation |
| `normalize_path_lexically` | Resolve lexical dot and parent components without filesystem access | `lexically_normal` |
| `make_lexically_relative_path` | Express one lexical path relative to a base path | No filesystem access |
| `collect_path_components` | Iterate over a path's individual components | Path iterators |
| `convert_path_to_generic_text` | Convert a path to text with portable separators | Generic path format |
| `check_path_exists_without_throwing` | Query existence while reporting errors through an output code | Non-throwing overload |
| `check_path_is_directory_without_throwing` | Test directory status while reporting query errors | Type predicate, non-throwing overload |
| `query_path_file_type` | Retrieve the followed target's file-type classification | Throwing `status` query |
| `query_symlink_file_type` | Retrieve a directory entry's own type without following a symlink | `symlink_status` semantics |
| `read_symlink_target` | Read the stored target path without following a symbolic link | Non-throwing overload |
| `make_absolute_path` | Resolve a path against the implementation's current path | Throwing absolute conversion |
| `canonicalize_existing_path` | Resolve an existing path completely while reporting errors | Non-throwing canonicalization |
| `weakly_canonicalize_path` | Canonicalize the existing prefix of a partly missing path | Weak canonicalization |
| `make_filesystem_relative_path` | Compute a base-relative path using filesystem resolution | Non-throwing `relative` |
| `check_paths_equivalent` | Test whether two paths resolve to the same filesystem object | Non-throwing equivalence query |
| `create_nested_directories` | Create all missing directories in a path without throwing | Creation result, error code |
| `copy_file_overwriting` | Copy one file and replace an existing destination without throwing | Copy options, error code |
| `copy_directory_tree` | Recursively copy a directory and overwrite regular destination files | Combined copy options, error code |
| `resize_file_without_throwing` | Change a regular file to a requested byte size | Non-throwing mutation |
| `rename_path_without_throwing` | Rename or move a filesystem entry and return its error status | Non-throwing mutation |
| `remove_one_path` | Remove one file or empty directory without throwing | Boolean removal result |
| `remove_path_tree` | Recursively remove a path tree and report the removed count | Non-throwing recursive mutation |
| `add_path_permissions` | Add permission bits without replacing existing permissions | Permission options, error code |
| `query_last_write_time` | Read a path's filesystem-clock modification time without throwing | `file_time_type` |
| `set_last_write_time` | Update a path's filesystem-clock modification time without throwing | `file_time_type` |
| `query_available_space` | Read available bytes for the filesystem containing a path | `space_info`, error code |
| `collect_directory_filenames` | Collect direct child filenames from a directory | `directory_iterator` |
| `collect_regular_file_paths` | Filter direct directory entries by regular-file status | `directory_entry` query |
| `collect_recursive_paths` | Traverse all descendants of a directory | `recursive_directory_iterator` |
| `skip_named_directory_subtrees` | Prevent recursive traversal beneath selected directory entries | Recursion control |
| `collect_directory_paths_with_errors` | Advance a directory iterator while reporting construction or increment errors | Manual non-throwing iteration |
