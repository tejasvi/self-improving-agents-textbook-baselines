from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        m = len(grid)
        NEG = float("-inf")
        # rows_with[v] = bitmask of rows containing value v
        rows_with = {}
        for i, row in enumerate(grid):
            for v in row:
                rows_with[v] = rows_with.get(v, 0) | (1 << i)

        full = 1 << m
        dp = [NEG] * full
        dp[0] = 0
        for v in sorted(rows_with):
            new = dp[:]  # skip value v
            avail = rows_with[v]
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                for i in range(m):
                    if (avail >> i) & 1 and not (mask >> i) & 1:
                        nm = mask | (1 << i)
                        if dp[mask] + v > new[nm]:
                            new[nm] = dp[mask] + v
            dp = new
        return int(max(x for x in dp if x != NEG))
