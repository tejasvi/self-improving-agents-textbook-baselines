from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        m = len(grid)
        # value -> bitmask of rows containing that value
        rows_of = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_of[v] = rows_of.get(v, 0) | (1 << r)

        NEG = -1
        full = 1 << m
        dp = [NEG] * full  # dp[mask] = max score using exactly rows in mask
        dp[0] = 0
        for v in sorted(rows_of):
            cand = rows_of[v]
            new_dp = dp[:]
            for mask in range(full):
                if dp[mask] < 0:
                    continue
                avail = cand & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    val = dp[mask] + v
                    if val > new_dp[nm]:
                        new_dp[nm] = val
            dp = new_dp
        return max(dp)
