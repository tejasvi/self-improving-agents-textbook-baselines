"""
Solution for the "maximize-value-of-function-in-a-ball-passing-game" problem.
We are given a functional graph defined by `receiver`, where each player i passes the ball
to `receiver[i]`. Starting from any player x we make exactly k passes, which means we
visit k+1 player ids (the starting player plus the k receivers). The value of a
starting player x is the sum of those visited ids.
We need the maximum possible value over all choices of x.

Constraints:
- n = len(receiver) ≤ 1e5
- k ≤ 1e10

Approach
----------
The graph is a collection of directed cycles with trees feeding into them. A direct
simulation for each start would be O(k) which is impossible for large k.
Instead we use binary lifting (doubling). For every node we pre‑compute:
    up[v][p]   – the node reached after 2^p moves starting from v.
    sum[v][p]  – the sum of the visited ids during those 2^p moves, **including**
                 the starting node of the segment but **excluding** the node
                 we land on after the segment.

With these tables the sum of the first `len` visited ids from a start node can be
obtained by decomposing `len` into powers of two (standard binary lifting).
The length we need is `k + 1` because the start node counts as the first visited
player.
The preprocessing costs O(n·logK) time and memory, and the final scan over all
starting nodes also costs O(n·logK) – well within the limits.
"""

from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        LOG = (k + 1).bit_length()  # enough bits to cover k+1 steps
        # up[v][p] = node after 2^p moves from v
        up = [[0] * LOG for _ in range(n)]
        # sum[v][p] = sum of visited ids during those 2^p moves (including start)
        sm = [[0] * LOG for _ in range(n)]

        # Base (p = 0) corresponds to a segment of length 1 (just the starting node)
        for v in range(n):
            up[v][0] = receiver[v]            # node after one move
            sm[v][0] = v                       # sum of the single visited node

        # Build higher powers
        for p in range(1, LOG):
            for v in range(n):
                mid = up[v][p - 1]
                up[v][p] = up[mid][p - 1]
                sm[v][p] = sm[v][p - 1] + sm[mid][p - 1]

        def total_sum_from(start: int) -> int:
            """Return f(start) = sum of the first k+1 visited ids starting from `start`."""
            remain = k + 1  # number of visited ids we need (including start)
            cur = start
            total = 0
            p = LOG - 1
            while remain:
                while (1 << p) > remain:
                    p -= 1
                total += sm[cur][p]
                cur = up[cur][p]
                remain -= 1 << p
            return total

        best = 0
        for x in range(n):
            val = total_sum_from(x)
            if val > best:
                best = val
        return best
