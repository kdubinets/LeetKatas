# Minimum Lights to Illuminate a Road

An array `lights` describes a road with positions `0` through `n-1`. If `lights[i]=v>0`, a working bulb at `i` illuminates every position from `max(0,i-v)` through `min(n-1,i+v)`. A zero means no bulb. You may install bulbs at any positions; each new bulb illuminates its position and its immediate neighbors within the road. Return the fewest new bulbs needed to illuminate every position.

`1 <= n <= 100000`; `0 <= lights[i] <= n`.
