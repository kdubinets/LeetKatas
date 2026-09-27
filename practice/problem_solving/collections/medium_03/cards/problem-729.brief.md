# My Calendar I

Design a calendar supporting repeated `book(start,end)` calls. Each requested event occupies the **half-open** time interval `[start,end)`. Accept and store it only if it shares no time point with any previously accepted event; return whether it was accepted. A rejected event must leave the calendar unchanged.

`0 ≤ start < end ≤ 10^9`; at most 1,000 calls. Thus `[10,20)` and `[20,30)` may both be booked.
