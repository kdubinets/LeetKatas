#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
workspace_dir=$(cd -- "$script_dir/.." && pwd)
collection_argument=${1:-collections/core}
language_standard=${2:-c++20}
compiler=${CXX:-g++}

if [[ "$collection_argument" = /* ]]; then
    collection_dir=$collection_argument
else
    collection_dir=$workspace_dir/$collection_argument
fi

manifest=$collection_dir/exercise_manifest.md

if [[ ! -d "$collection_dir" ]]; then
    printf 'Collection directory does not exist: %s\n' "$collection_dir" >&2
    exit 1
fi

if [[ ! -f "$manifest" ]]; then
    printf 'Collection manifest does not exist: %s\n' "$manifest" >&2
    exit 1
fi

if ! command -v "$compiler" >/dev/null 2>&1; then
    printf 'Compiler is not available: %s\n' "$compiler" >&2
    exit 1
fi

mapfile -d '' sources < <(
    find "$collection_dir" -maxdepth 1 -type f -name '*.cpp' -print0 | sort -z
)

if (( ${#sources[@]} == 0 )); then
    printf 'No C++ exercises found in %s\n' "$collection_dir" >&2
    exit 1
fi

status=0

for source in "${sources[@]}"; do
    base_path=${source%.cpp}
    base_name=${base_path##*/}
    metadata=$base_path.md

    if [[ ! -f "$metadata" ]]; then
        printf 'MISSING METADATA: %s\n' "$base_name" >&2
        status=1
        continue
    fi

    marker_count=$(grep -Ec '^[[:space:]]*// Finish: ' "$source" || true)
    comment_count=$(grep -Ec '// ' "$source" || true)
    heading_count=$(grep -Ec '^# (Name|Description|Solution)$' "$metadata" || true)
    solution_fence_count=$(grep -Ec '^```cpp$' "$metadata" || true)

    if [[ "$marker_count" != 1 || "$comment_count" != 1 ||
          "$heading_count" != 3 || "$solution_fence_count" != 1 ]]; then
        printf 'STRUCTURE FAIL: %s markers=%s comments=%s headings=%s solution_fences=%s\n' \
            "$base_name" "$marker_count" "$comment_count" \
            "$heading_count" "$solution_fence_count" >&2
        status=1
        continue
    fi

    if ! grep -Fq "| \`$base_name\` |" "$manifest"; then
        printf 'NOT IN MANIFEST: %s\n' "$base_name" >&2
        status=1
    fi

    if ! awk -v metadata="$metadata" '
        BEGIN {
            capturing = 0
            while ((getline line < metadata) > 0) {
                if (!capturing && line == "```cpp") {
                    capturing = 1
                    continue
                }
                if (capturing && line == "```") {
                    break
                }
                if (capturing) {
                    solution[++solution_count] = line
                }
            }
            close(metadata)
            if (solution_count == 0) {
                exit 2
            }
        }
        /^[[:space:]]*\/\/ Finish: / {
            match($0, /^[[:space:]]*/)
            indent = substr($0, 1, RLENGTH)
            for (line_number = 1; line_number <= solution_count; ++line_number) {
                print indent solution[line_number]
            }
            next
        }
        { print }
    ' "$source" | "$compiler" -std="$language_standard" \
            -Wall -Wextra -Werror -x c++ -fsyntax-only -; then
        printf 'COMPILE FAIL: %s\n' "$base_name" >&2
        status=1
    fi
done

while IFS= read -r -d '' metadata; do
    metadata_name=${metadata##*/}
    case "$metadata_name" in
        collection_spec.md|exercise_manifest.md|README.md)
            continue
            ;;
    esac

    if [[ ! -f "${metadata%.md}.cpp" ]]; then
        printf 'UNPAIRED METADATA: %s\n' "$metadata_name" >&2
        status=1
    fi
done < <(find "$collection_dir" -maxdepth 1 -type f -name '*.md' -print0)

manifest_rows=$(grep -Ec '^\| `[^`]+` \|' "$manifest" || true)
if [[ "$manifest_rows" != "${#sources[@]}" ]]; then
    printf 'MANIFEST COUNT FAIL: exercises=%s rows=%s\n' \
        "${#sources[@]}" "$manifest_rows" >&2
    status=1
fi

primary_skill_duplicates=$(
    awk -F'|' '
        /^\| `[^`]+` \|/ {
            skill = $3
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", skill)
            print skill
        }
    ' "$manifest" | sort | uniq -d
)

if [[ -n "$primary_skill_duplicates" ]]; then
    printf 'DUPLICATE PRIMARY SKILLS:\n%s\n' \
        "$primary_skill_duplicates" >&2
    status=1
fi

if [[ "$status" != 0 ]]; then
    exit "$status"
fi

printf 'Validated %s exercises in %s with %s (%s).\n' \
    "${#sources[@]}" "$collection_argument" "$compiler" "$language_standard"
