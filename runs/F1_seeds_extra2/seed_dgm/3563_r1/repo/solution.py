from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        # Map each value to the set of rows (bitmask) in which it appears.
        rows_of = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_of[v] = rows_of.get(v, 0) | (1 << r)

        # dp[mask] = max score using distinct values, where `mask` is the set
        # of rows already used by selected cells.
        NEG = float("-inf")
        n = len(grid)
        dp = [NEG] * (1 << n)
        dp[0] = 0

        for v in sorted(rows_of):
            rmask = rows_of[v]
            new = dp[:]
            for mask in range(1 << n):
                if dp[mask] == NEG:
                    continue
                avail = rmask & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    cand = dp[mask] + v
                    if cand > new[nm]:
                        new[nm] = cand
            dp = new

        return int(max(dp))
