# Evaluate Division

You receive equations `A/B = value` between named variables and queries asking for `C/D`. Return each determined ratio, or `−1.0` when it cannot be determined. The equations are consistent and never require division by zero. A variable absent from **all equations** is undefined, even for a query of that variable divided by itself.

There are at most 20 equations and 20 queries; names are short alphanumeric strings. For equations `a/b=2` and `b/c=3`, `a/c=6`, while unknown `x/x=−1`.
