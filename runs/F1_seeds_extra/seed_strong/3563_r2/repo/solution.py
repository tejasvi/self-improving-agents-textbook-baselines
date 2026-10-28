from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for i, row in enumerate(grid):
            for v in row:
                rows_with[v] |= 1 << i
        NEG = float('-inf')
        size = 1 << n
        dp = [NEG] * size
        dp[0] = 0
        for v in range(1, 101):
            if rows_with[v] == 0:
                continue
            new = dp[:]
            avail = rows_with[v]
            for mask in range(size):
                if dp[mask] == NEG:
                    continue
                cand = avail & ~mask
                while cand:
                    b = cand & -cand
                    cand ^= b
                    nm = mask | b
                    val = dp[mask] + v
                    if val > new[nm]:
                        new[nm] = val
            dp = new
        return int(max(dp))
