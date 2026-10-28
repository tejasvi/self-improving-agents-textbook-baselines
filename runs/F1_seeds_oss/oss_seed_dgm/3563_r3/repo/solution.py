from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """Return the maximum possible sum selecting at most one cell per row
        such that all selected values are distinct.
        """
        # Number of rows
        n = len(grid)
        # For each row, we will consider its unique values (duplicates within a row are irrelevant)
        rows = [list(set(row)) for row in grid]
        # Sort rows to improve pruning: rows with larger potential values first
        rows.sort(key=lambda r: -max(r) if r else 0)

        best = 0
        used = set()

        # Pre‑compute the maximum possible additional sum from remaining rows (optimistic bound)
        # For each row we take its maximum value (ignoring uniqueness), then prefix sums.
        max_per_row = [max(r) if r else 0 for r in rows]
        suffix_best = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_best[i] = suffix_best[i + 1] + max_per_row[i]

        def dfs(idx: int, cur_sum: int) -> None:
            nonlocal best
            # If we have processed all rows, update best
            if idx == n:
                if cur_sum > best:
                    best = cur_sum
                return
            # Prune if even taking the optimistic maximum cannot beat current best
            if cur_sum + suffix_best[idx] <= best:
                return
            # Option 1: skip this row
            dfs(idx + 1, cur_sum)
            # Option 2: try each value in this row that is not used yet
            for val in rows[idx]:
                if val in used:
                    continue
                used.add(val)
                dfs(idx + 1, cur_sum + val)
                used.remove(val)

        dfs(0, 0)
        return best
