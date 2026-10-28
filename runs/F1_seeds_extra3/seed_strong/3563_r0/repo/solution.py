from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] = rows_with.get(v, 0) | (1 << r)
        NEG = -1
        dp = [NEG] * (1 << n)
        dp[0] = 0
        for v in sorted(rows_with):
            m = rows_with[v]
            new = dp[:]
            for mask in range(1 << n):
                if dp[mask] < 0:
                    continue
                avail = m & ~mask
                while avail:
                    low = avail & -avail
                    avail ^= low
                    nm = mask | low
                    cand = dp[mask] + v
                    if cand > new[nm]:
                        new[nm] = cand
            dp = new
        return max(dp)
