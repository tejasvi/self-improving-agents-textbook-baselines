from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] = rows_with.get(v, 0) | (1 << r)

        NEG = float("-inf")
        full = 1 << n
        # dp[mask] = max score where rows in mask have been assigned distinct values
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
                    val = dp[mask] + v
                    if val > new[nm]:
                        new[nm] = val
            dp = new
        return int(max(dp))
