# Task Scheduler

A CPU has tasks labeled by uppercase letters. In one interval it completes one task or idles. Tasks may run in any order, but two tasks with the same label must have at least `n` **intervening intervals** between them. Return the fewest intervals needed to complete all tasks. There are 1–10,000 tasks and `n` is between 0 and 100.

For `A,A,A,B,B,B` with `n=2`, a schedule `A,B,idle,A,B,idle,A,B` takes 8 intervals.
