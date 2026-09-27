# Best Time to Buy and Sell Stock V

Given stock prices for successive days and integer `k`, earn the greatest total profit using at most `k` completed transactions. A normal transaction buys on day `i` and sells on a later day `j`, earning `prices[j]-prices[i]`. A short transaction sells on day `i` and buys back on a later day `j`, earning `prices[i]-prices[j]`. Complete each transaction before opening another; a day closing one transaction cannot open the next. Return the maximum profit.

`2 <= n <= 1000`; `1 <= prices[i] <= 10^9`; `1 <= k <= floor(n/2)`.
