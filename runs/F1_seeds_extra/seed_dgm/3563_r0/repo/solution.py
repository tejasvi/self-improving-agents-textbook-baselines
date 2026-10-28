from typing import List


class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        # rows_of[v] = bitmask of rows containing value v
        rows_of = {}
        for r, row in enumerate(grid):
            for v in row:
                rows_of[v] = rows_of.get(v, 0) | (1 << r)

        # dp: row-mask -> best score; each value used at most once
        dp = {0: 0}
        for v in sorted(rows_of):
            new = dict(dp)
            rmask = rows_of[v]
            for mask, score in dp.items():
                avail = rmask & ~mask
                while avail:
                    bit = avail & -avail
                    avail ^= bit
                    nm = mask | bit
                    ns = score + v
                    if new.get(nm, -1) < ns:
                        new[nm] = ns
            dp = new
        return max(dp.values())
