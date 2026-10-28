from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """Return the maximum possible sum of selected cells such that
        - No two selected cells are from the same row.
        - All selected values are distinct.
        """
        if not grid:
            return 0
        rows = len(grid)
        cols = len(grid[0])
        # Gather all distinct values in the grid
        distinct_vals = sorted({grid[i][j] for i in range(rows) for j in range(cols)})
        vcnt = len(distinct_vals)
        # We add one dummy column (value 0) to allow skipping a row.
        n = max(rows, vcnt + 1)  # size of square matrix for Hungarian algorithm
        # Map each distinct value to a column index
        val_to_idx = {v: idx for idx, v in enumerate(distinct_vals)}
        # Build weight matrix (rows x n). Rows beyond actual rows are dummy and stay zero.
        weight = [[0] * n for _ in range(n)]
        for i in range(rows):
            for j in range(cols):
                v = grid[i][j]
                idx = val_to_idx[v]
                weight[i][idx] = v  # if multiple cells in same row have same value, weight stays v
        # Hungarian algorithm works with a cost matrix that we want to minimize.
        # To maximize sum of selected values we use cost = -weight.
        INF = 10 ** 9
        cost = [[0] * (n + 1) for _ in range(n + 1)]  # 1‑based indexing
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                cost[i][j] = -weight[i - 1][j - 1]
        # Implementation of the Hungarian algorithm (O(n^3))
        u = [0] * (n + 1)
        v = [0] * (n + 1)
        p = [0] * (n + 1)
        way = [0] * (n + 1)
        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            minv = [INF] * (n + 1)
            used = [False] * (n + 1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = INF
                j1 = 0
                for j in range(1, n + 1):
                    if not used[j]:
                        cur = cost[i0][j] - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                for j in range(0, n + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            # Augmenting path
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break
        # Reconstruct the assignment and compute the maximal sum.
        total = 0
        for j in range(1, n + 1):
            i = p[j]
            # i is the row (1‑based) assigned to column j.
            if i == 0 or i > rows:
                continue
            col_idx = j - 1
            if col_idx < vcnt:  # real value column
                total += weight[i - 1][col_idx]
            # else dummy column -> contributes 0
        return total
