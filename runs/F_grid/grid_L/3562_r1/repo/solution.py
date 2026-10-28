from typing import List
from bisect import bisect_right


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        order = sorted(range(n), key=lambda i: intervals[i][0])
        starts = [intervals[i][0] for i in order]
        # nxt[p]: first sorted position whose start is strictly greater than end of order[p]
        nxt = [bisect_right(starts, intervals[order[p]][1]) for p in range(n)]

        K = 4

        def better(a, b):
            # a, b are (score, tuple); higher score wins, then lexicographically smaller tuple
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        # F[j][p]: best (score, sorted index tuple) using up to j intervals among sorted positions >= p
        empty = (0, ())
        prev = [empty] * (n + 1)  # F[0]
        for j in range(1, K + 1):
            cur = [empty] * (n + 1)
            for p in range(n - 1, -1, -1):
                idx = order[p]
                w = intervals[idx][2]
                s, t = prev[nxt[p]]
                take = (w + s, tuple(sorted(t + (idx,))))
                cur[p] = better(cur[p + 1], take)
            prev = cur
        return list(prev[0][1])
