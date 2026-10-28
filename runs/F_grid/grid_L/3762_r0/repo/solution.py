from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(k: int) -> bool:
            if k == 0:
                return True
            T = [2 * (-(-k // p)) for p in points]
            # P[p]: crossings of edge p-1 (edges left of final pos e), odd, greedy from left
            P = [0] * (n + 1)
            P[0] = 1
            for i in range(n):
                v = max(1, T[i] - P[i])
                if v % 2 == 0:
                    v += 1
                P[i + 1] = v
            # Q[p]: crossings of edge p-1 (edges right of e), even >= 2, greedy from right
            Q = [0] * (n + 1)
            for i in range(n - 1, 0, -1):
                v = max(2, T[i] - Q[i + 1])
                if v % 2 == 1:
                    v += 1
                Q[i] = v
            preP = [0] * (n + 1)
            s = 0
            for p in range(n + 1):
                s += P[p]
                preP[p] = s
            sufQ = [0] * (n + 2)
            s = 0
            for p in range(n, -1, -1):
                s += Q[p]
                sufQ[p] = s
            for e in range(n):
                d = T[e] - 1 - P[e] - Q[e + 1]
                extra = 2 * ((d + 1) // 2) if d > 0 else 0
                if preP[e] + sufQ[e + 1] + extra <= m:
                    return True
            return False

        lo, hi = 0, m * max(points) + 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
