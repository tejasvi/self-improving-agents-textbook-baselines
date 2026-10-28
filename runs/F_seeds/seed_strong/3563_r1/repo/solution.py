from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        NEG = float('-inf')
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for r, row in enumerate(grid):
            for x in row:
                rows_with[x] |= 1 << r
        dp = [NEG] * (1 << n)
        dp[0] = 0
        for v in range(1, 101):
            rw = rows_with[v]
            if not rw:
                continue
            new = dp[:]
            for mask in range(1 << n):
                cur = dp[mask]
                if cur == NEG:
                    continue
                avail = rw & ~mask
                while avail:
                    low = avail & -avail
                    nm = mask | low
                    if cur + v > new[nm]:
                        new[nm] = cur + v
                    avail ^= low
            dp = new
        return int(max(dp[1:]))
