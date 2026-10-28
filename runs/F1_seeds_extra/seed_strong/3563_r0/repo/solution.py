from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for r, row in enumerate(grid):
            for v in row:
                rows_with[v] |= 1 << r
        NEG = -1
        full = 1 << n
        dp = [NEG] * full
        dp[0] = 0
        for v in range(1, 101):
            rw = rows_with[v]
            if not rw:
                continue
            new = dp[:]  # skip value v
            for mask in range(full):
                cur = dp[mask]
                if cur < 0:
                    continue
                avail = rw & ~mask
                while avail:
                    low = avail & -avail
                    nm = mask | low
                    if new[nm] < cur + v:
                        new[nm] = cur + v
                    avail ^= low
            dp = new
        return max(dp)
