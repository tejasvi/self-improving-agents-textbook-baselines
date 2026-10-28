from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # value -> bitmask of rows containing that value
        rows_of = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_of[v] = rows_of.get(v, 0) | (1 << r)

        NEG = float("-inf")
        full = 1 << n
        dp = [NEG] * full  # dp[mask]: max score using rows in mask, values processed so far
        dp[0] = 0
        for v in sorted(rows_of):
            cand = rows_of[v]
            new = dp[:]  # option: skip value v
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                avail = cand & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    if dp[mask] + v > new[nm]:
                        new[nm] = dp[mask] + v
            dp = new
        return int(max(dp))
