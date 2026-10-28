from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] |= 1 << r
        NEG = float("-inf")
        full = 1 << n
        dp = [NEG] * full
        dp[0] = 0
        for v in range(1, 101):
            if not rows_with[v]:
                continue
            new = dp[:]  # skip value v
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                avail = rows_with[v] & ~mask
                while avail:
                    b = avail & -avail
                    avail ^= b
                    nm = mask | b
                    if dp[mask] + v > new[nm]:
                        new[nm] = dp[mask] + v
            dp = new
        return int(max(dp))
