# Capacity To Ship Packages Within D Days

Packages with positive weights must be shipped **in their given order**. Each day a ship takes a contiguous next portion whose total weight is at most its fixed capacity. Given the weights and a maximum number of days, return the smallest capacity that lets all packages be shipped in time. There are at most 50,000 packages, each weighing 1–500, and `days` is between 1 and the package count.

For weights `[3,2,2,4,1,4]` and 3 days, capacity 6 permits daily groups `[3,2]`, `[2,4]`, `[1,4]`; smaller capacities do not suffice.
