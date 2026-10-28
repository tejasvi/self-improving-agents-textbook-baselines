from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        # Map each distinct value to the bitmask of rows containing it.
        value_rows = {}
        for r, row in enumerate(grid):
            for v in row:
                value_rows[v] = value_rows.get(v, 0) | (1 << r)

        n = len(grid)
        NEG = float("-inf")
        # dp[mask] = max score where rows in mask have each been assigned one distinct value
        dp = [NEG] * (1 << n)
        dp[0] = 0
        for v in sorted(value_rows):
            rows = value_rows[v]
            new_dp = dp[:]  # option: skip value v
            for mask in range(1 << n):
                if dp[mask] == NEG:
                    continue
                avail = rows & ~mask
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
