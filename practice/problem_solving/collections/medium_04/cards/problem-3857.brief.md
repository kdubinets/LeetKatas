# Minimum Cost to Split into Ones

Start with the integer `n`. In one operation, choose any current integer `v>1`, split it into two **positive** integers `a` and `b` with `a+b=v`, and pay `a×b`. Continue until all pieces are 1. Return the minimum possible total cost. `n` is between 1 and 500.

For `n=4`, splitting into 2 and 2, then splitting both 2s, costs `4+1+1=6`.
