from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # value -> bitmask of rows containing that value
        val_rows = {}
        for r, row in enumerate(grid):
            for v in row:
                val_rows[v] = val_rows.get(v, 0) | (1 << r)

        NEG = float('-inf')
        full = 1 << n
        dp = [NEG] * full  # dp[mask] = best score using rows in mask, one value per row
        dp[0] = 0
        for v in sorted(val_rows):
            rows = val_rows[v]
            new = dp[:]
            for mask in range(full):
                if dp[mask] == NEG:
                    continue
                for r in range(n):
                    if (rows >> r) & 1 and not (mask >> r) & 1:
                        nm = mask | (1 << r)
                        if dp[mask] + v > new[nm]:
                            new[nm] = dp[mask] + v
            dp = new
        return int(max(dp))
