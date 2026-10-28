"""Solution for selecting cells in grid with maximum score.
We need to select at most one cell per row, with all selected values distinct, maximizing sum.
Implemented via a maximum weight bipartite matching (Hungarian algorithm).
"""

from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        # Number of rows
        n = len(grid)
        # Collect distinct values
        distinct_vals = []
        val_to_idx = {}
        for row in grid:
            for v in row:
                if v not in val_to_idx:
                    val_to_idx[v] = len(distinct_vals)
                    distinct_vals.append(v)
        m = len(distinct_vals)  # number of distinct values
        # Size of square matrix for Hungarian: rows + values (allow dummy matches)
        N = n + m
        # Initialize weight matrix with zeros
        weight = [[0] * N for _ in range(N)]
        # Fill real rows (0..n-1) with real values (0..m-1)
        for i, row in enumerate(grid):
            for v in row:
                j = val_to_idx[v]
                weight[i][j] = v  # if multiple occurrences, same weight
        # The remaining cells (including dummy rows/cols) stay zero.
        # Hungarian algorithm for maximum weight matching on square matrix.
        def hungarian(a: List[List[int]]) -> int:
            n = len(a)
            # potentials
            u = [0] * (n + 1)
            v = [0] * (n + 1)
            p = [0] * (n + 1)  # matching for columns, p[j] = i matched to j
            way = [0] * (n + 1)
            for i in range(1, n + 1):
                p[0] = i
                j0 = 0
                minv = [float('inf')] * (n + 1)
                used = [False] * (n + 1)
                while True:
                    used[j0] = True
                    i0 = p[j0]
                    delta = float('inf')
                    j1 = 0
                    for j in range(1, n + 1):
                        if not used[j]:
                            # For maximization we use -a[i0-1][j-1]
                            cur = -a[i0 - 1][j - 1] - u[i0] - v[j]
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
                # augmenting
                while True:
                    j1 = way[j0]
                    p[j0] = p[j1]
                    j0 = j1
                    if j0 == 0:
                        break
            # Build assignment list: row i assigned to column assignment[i]
            assignment = [-1] * n
            for j in range(1, n + 1):
                if p[j] != 0:
                    assignment[p[j] - 1] = j - 1
            total = 0
            for i in range(n):
                j = assignment[i]
                if j != -1:
                    total += a[i][j]
            return total

        max_sum = hungarian(weight)
        return max_sum
