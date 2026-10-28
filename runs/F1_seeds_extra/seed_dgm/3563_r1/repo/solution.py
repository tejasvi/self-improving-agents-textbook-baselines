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
        dp = [NEG] * (1 << m)
        dp[0] = 0
        # Each value can be used at most once; process values one by one (0/1 knapsack style).
        for v in sorted(rows_with, reverse=True):
            mask_rows = rows_with[v]
            new_dp = dp[:]
            for mask in range(1 << m):
                if dp[mask] == NEG:
                    continue
                avail = mask_rows & ~mask
                r = 0
                while avail:
                    if avail & 1:
                        nm = mask | (1 << r)
                        if dp[mask] + v > new_dp[nm]:
                            new_dp[nm] = dp[mask] + v
                    avail >>= 1
                    r += 1
            dp = new_dp
        return int(max(dp))
