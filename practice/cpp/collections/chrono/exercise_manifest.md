# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `cast_duration_units` | Explicitly convert a duration to a coarser integral unit | `duration_cast`, truncation |
| `add_mixed_durations` | Add durations with different periods into their common unit | Common duration type |
| `compare_mixed_durations` | Compare durations without manually normalizing units | Type-safe relational operation |
| `absolute_duration` | Obtain the nonnegative magnitude of a signed duration | `chrono::abs` |
| `floor_duration` | Round a duration downward to a coarser unit | Negative duration behavior |
| `ceil_duration` | Round a duration upward to a coarser unit | Negative duration behavior |
| `round_duration` | Round a duration to the nearest coarser unit | Half-to-even behavior |
| `duration_remainder` | Compute elapsed time remaining after whole intervals | Mixed duration periods |
| `construct_duration_with_literals` | Compose a duration from C++ chrono literals | Seconds and milliseconds literals |
| `offset_steady_time_point` | Add a duration to a monotonic-clock time point | Future instant calculation |
| `measure_elapsed_duration` | Subtract monotonic-clock time points | Signed elapsed duration |
| `check_deadline_reached` | Compare a current time point with a deadline | Inclusive deadline boundary |
| `clamp_remaining_duration` | Return nonnegative time remaining before a deadline | Duration zero, conditional result |
| `ceil_timeout_milliseconds` | Convert a positive remaining duration without shortening a timeout | Duration ceiling |
| `cast_time_point_precision` | Truncate a time point to millisecond precision | `time_point_cast` |
| `convert_system_time_to_time_t` | Cross from a system-clock time point to the C time representation | Clock boundary |
| `convert_time_t_to_system_time` | Cross from the C time representation to a system-clock time point | Clock boundary |
| `construct_calendar_date` | Construct a civil date from numeric year, month, and day fields | Strong calendar field types |
| `validate_calendar_date` | Test whether a civil date denotes a real calendar day | `year_month_day::ok` |
| `convert_date_to_sys_days` | Map a valid civil date onto the system-day timeline | Day-precision time point |
| `convert_sys_days_to_date` | Recover civil calendar fields from a system-day value | `year_month_day` conversion |
| `extract_date_from_system_time` | Obtain the civil date containing a system-clock instant | Day floor, pre-epoch behavior |
| `combine_date_and_time` | Compose a civil date and time fields into a system-clock point | `sys_days`, mixed durations |
| `shift_calendar_by_days` | Move a valid civil date by an exact count of days | Timeline arithmetic |
| `difference_between_calendar_dates` | Measure the signed day distance between civil dates | `sys_days`, date subtraction |
| `shift_calendar_by_months` | Shift calendar month fields while retaining the day field | Possible invalid result |
| `difference_between_year_months` | Measure the signed month distance between calendar months | `year_month` arithmetic |
| `find_last_day_of_month` | Obtain the final numbered day for a year and month | Leap-year-aware month end |
| `find_date_weekday` | Determine the weekday of a valid civil date | `weekday`, `sys_days` |
| `find_weekday_on_or_after` | Find the first requested weekday not before a date | Weekday difference, day shift |
| `make_nth_weekday_of_month` | Represent an indexed weekday within a year and month | `weekday_indexed` |
| `validate_indexed_weekday` | Test whether an indexed weekday occurrence exists in a month | Calendar validity |
| `make_last_weekday_of_month` | Represent the final requested weekday within a year and month | `weekday_last` |
| `check_calendar_leap_year` | Query whether a calendar year is a leap year | Strong year type |
| `split_time_of_day` | Decompose a since-midnight duration into clock fields | `hh_mm_ss`, subsecond precision |
| `read_time_of_day_fields` | Extract typed fields from an `hh_mm_ss` value | Tuple, duration accessors |
