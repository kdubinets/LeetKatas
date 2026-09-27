# Count Zero Request Servers

Given `n` servers numbered `1` through `n`, logs `[server_id,time]`, a positive duration `x`, and query times, return for each query `q` the number of servers with no request logged in the inclusive interval `[q-x,q]`. Logs and queries need not be sorted. Repeated requests and repeated query times are allowed. Return answers in query input order.

`1 <= n, |logs|, |queries| <= 10^5`; log times lie in `[1,10^6]`; `1 <= x <= 10^5`; `x < q <= 10^6`.
