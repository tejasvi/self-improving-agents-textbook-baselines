from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        m = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] = rows_with.get(v, 0) | (1 << r)

        NEG = float("-inf")
        full = 1 << m
        # dp[mask] = max score where mask is the set of rows already used
        dp = [NEG] * full
        dp[0] = 0
        for v in sorted(rows_with):
            cand = rows_with[v]
            new = dp[:]  # skip value v
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                avail = cand & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    if dp[mask] + v > new[nm]:
                        new[nm] = dp[mask] + v
            dp = new
        return int(max(dp))
