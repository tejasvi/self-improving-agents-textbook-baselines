from typing import List


class Solution:
    def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
        n = len(fruits)
        # First child takes the main diagonal.
        ans = sum(fruits[i][i] for i in range(n))

        NEG = float("-inf")

        def upper(grid):
            # Child starting at (0, n-1) moving down with column change -1/0/+1,
            # restricted to cells with j > i (strictly above the diagonal).
            # Ends at (n-1, n-1), which is already counted on the diagonal.
            dp = [NEG] * n
            dp[n - 1] = grid[0][n - 1]
            for i in range(1, n - 1):
                ndp = [NEG] * n
                for j in range(i + 1, n):
                    best = NEG
                    for pj in (j - 1, j, j + 1):
                        if 0 <= pj < n and dp[pj] > best:
                            best = dp[pj]
                    if best != NEG:
                        ndp[j] = best + grid[i][j]
                dp = ndp
            # Final step to (n-1, n-1): nothing extra to add.
            best = NEG
            for pj in (n - 2, n - 1):
                if 0 <= pj < n and dp[pj] > best:
                    best = dp[pj]
            return 0 if best == NEG else best

        a = upper(fruits)
        transposed = [list(r) for r in zip(*fruits)]
        b = upper(transposed)
        return ans + a + b
