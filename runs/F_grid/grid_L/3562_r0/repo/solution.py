from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        K = 4
        # Sort by right endpoint; intervals compatible with sorted interval m-1
        # (those with r < l) form a prefix of length pre[m].
        order = sorted(range(n), key=lambda i: intervals[i][1])
        rs = [intervals[i][1] for i in order]
        pre = [0] * (n + 1)
        for m in range(1, n + 1):
            l = intervals[order[m - 1]][0]
            pre[m] = bisect_left(rs, l)

        # dp[m][c]: best (weight, sorted index tuple) choosing exactly c
        # intervals among the first m sorted ones; None if infeasible.
        # Preference: max weight, then lexicographically smallest tuple.
        def better(a, b):
            if a is None:
                return b
            if b is None:
                return a
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        dp = [[None] * (K + 1) for _ in range(n + 1)]
        dp[0][0] = (0, ())
        for m in range(1, n + 1):
            orig = order[m - 1]
            w = intervals[orig][2]
            p = pre[m]
            row = dp[m]
            prow = dp[m - 1]
            trow = dp[p]
            row[0] = (0, ())
            for c in range(1, K + 1):
                cand = prow[c]
                take = trow[c - 1]
                if take is not None:
                    cand = better(
                        cand,
                        (take[0] + w, tuple(sorted(take[1] + (orig,)))),
                    )
                row[c] = cand

        best = None
        for c in range(K + 1):
            best = better(best, dp[n][c])
        return list(best[1])
