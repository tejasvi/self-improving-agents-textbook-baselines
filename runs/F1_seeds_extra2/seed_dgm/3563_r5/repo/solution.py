from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        m = len(grid)
        full = 1 << m
        NEG = float("-inf")
        # rows_with[v] = bitmask of rows containing value v
        rows_with = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] = rows_with.get(v, 0) | (1 << r)
        # dp[mask] = max score using values processed so far, where mask = rows used
        dp = [NEG] * full
        dp[0] = 0
        for v in sorted(rows_with):
            cand = rows_with[v]
            ndp = dp[:]  # skip value v
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                avail = cand & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    val = dp[mask] + v
                    if val > ndp[nm]:
                        ndp[nm] = val
            dp = ndp
        return int(max(dp))
