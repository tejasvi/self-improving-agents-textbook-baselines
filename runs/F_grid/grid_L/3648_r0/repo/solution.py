from typing import List


class Solution:
    def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
        n = len(fruits)
        NEG = float("-inf")

        # First child: main diagonal.
        total = sum(fruits[i][i] for i in range(n))

        def upper(grid):
            # Child starting at (0, n-1) moving to (i+1, j-1|j|j+1),
            # restricted to cells with j > i (strictly above the diagonal),
            # plus the final cell (n-1, n-1) which is on the diagonal.
            dp = [NEG] * n
            dp[n - 1] = grid[0][n - 1]
            for i in range(1, n - 1):
                nd = [NEG] * n
                for j in range(i + 1, n):
                    best = max(dp[j - 1] if j - 1 >= 0 else NEG,
                               dp[j],
                               dp[j + 1] if j + 1 < n else NEG)
                    if best != NEG:
                        nd[j] = best + grid[i][j]
                dp = nd
            # Last step into (n-1, n-1) from row n-2, column n-2 or n-1.
            best = max(dp[n - 2], dp[n - 1]) if n >= 2 else NEG
            return 0 if best == NEG else best

        # Second child: upper triangle.
        res = upper(fruits)
        # Third child: lower triangle, via transpose.
        transposed = [list(row) for row in zip(*fruits)]
        res += upper(transposed)
        return total + res
