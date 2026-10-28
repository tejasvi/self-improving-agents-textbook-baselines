from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for i, row in enumerate(grid):
            for x in row:
                rows_with[x] |= 1 << i
        NEG = -1
        full = 1 << n
        dp = [NEG] * full  # dp[mask] = max score using chosen rows exactly mask
        dp[0] = 0
        for v in range(1, 101):
            rw = rows_with[v]
            if not rw:
                continue
            new = dp[:]
            for mask in range(full):
                cur = dp[mask]
                if cur < 0:
                    continue
                avail = rw & ~mask
                while avail:
                    low = avail & -avail
                    nm = mask | low
                    if cur + v > new[nm]:
                        new[nm] = cur + v
                    avail ^= low
            dp = new
        return max(dp)
