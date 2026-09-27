# Maximize Sum of Device Ratings

There are `m` devices, each initially holding exactly `n` positive-capacity units. A device's rating is its **minimum** unit capacity, or 0 if empty. One operation removes exactly one unit from a device that has never been used as a source, puts it in a different device, and marks that source as used. A device may receive any number of units and may later be a source. Return the maximum possible sum of final device ratings; zero operations are allowed. There are at most 200,000 units in total, and each capacity is at most 100,000.
