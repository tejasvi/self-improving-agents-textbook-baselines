from typing import *


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # rows_with[v] = bitmask of rows containing value v
        rows_with = [0] * 101
        for r, row in enumerate(grid):
            for x in row:
                rows_with[x] |= 1 << r
        NEG = float('-inf')
        full = 1 << n
        dp = [NEG] * full
        dp[0] = 0
        for v in range(1, 101):
            rw = rows_with[v]
            if not rw:
                continue
            ndp = dp[:]
            for mask in range(full):
                cur = dp[mask]
                if cur == NEG:
                    continue
                avail = rw & ~mask
                while avail:
                    b = avail & -avail
                    avail ^= b
                    nm = mask | b
                    if cur + v > ndp[nm]:
                        ndp[nm] = cur + v
            dp = ndp
        return int(max(dp))
