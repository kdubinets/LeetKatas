# Name

Minimum Rooms for Half-Open Meetings

# Description

Return the minimum rooms needed for half-open meetings. Every start is before its end; an end at the same time as another start releases its room first. Empty input needs zero rooms and input is preserved.

The supplied event sweep sorts endpoint deltas with end events before starts at equal times and records maximum active count.

This exercise covers equal-time event ordering while maintaining maximum concurrency.

# Solution

```cpp
std::vector<std::pair<int, int>> events;
events.reserve(meetings.size() * 2);
for (const Interval& meeting : meetings) {
    events.emplace_back(meeting.start, 1);
    events.emplace_back(meeting.end, -1);
}
std::sort(events.begin(), events.end());
std::size_t active = 0;
std::size_t greatest = 0;
for (const auto& [time, delta] : events) {
    static_cast<void>(time);
    if (delta < 0) {
        --active;
    } else {
        ++active;
        greatest = std::max(greatest, active);
    }
}
return greatest;
```
