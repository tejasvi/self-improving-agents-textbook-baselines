from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        # Map each distinct value to a column index
        value_to_col = {}
        for row in grid:
            for v in row:
                if v not in value_to_col:
                    value_to_col[v] = len(value_to_col)
        rows = len(grid)
        cols = len(value_to_col)
        n = max(rows, cols)  # size of square matrix for Hungarian
        # Build weight matrix (1-indexed for algorithm)
        w = [[0] * (n + 1) for _ in range(n + 1)]
        for i, row in enumerate(grid):
            for v in row:
                j = value_to_col[v]
                w[i + 1][j + 1] = v  # weight for row i+1, column j+1
        # Hungarian algorithm for maximum weight matching (allow dummy columns with weight 0)
        INF = 10 ** 12
        u = [0] * (n + 1)
        v = [0] * (n + 1)
        p = [0] * (n + 1)      # p[j] = row assigned to column j
        way = [0] * (n + 1)
        for i in range(1, rows + 1):  # only real rows need to be matched
            p[0] = i
            j0 = 0
            minv = [INF] * (n + 1)
            used = [False] * (n + 1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = INF
                j1 = 0
                # iterate over all columns (including dummy ones)
                for j in range(1, n + 1):
                    if not used[j]:
                        cur = -(w[i0][j]) - u[i0] - v[j]  # negative because we maximize
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                # update potentials
                for j in range(0, n + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            # augmenting path
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break
        # Compute total weight of matches that involve real rows and real value columns
        total = 0
        for j in range(1, n + 1):
            i = p[j]
            if 1 <= i <= rows and 1 <= j <= cols:
                total += w[i][j]
        return total
