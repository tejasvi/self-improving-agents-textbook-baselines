from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(k: int) -> bool:
            # c[i]: required number of visits to index i so that points[i]*visits >= k
            c = [(k + p - 1) // p for p in points]

            # Left greedy: xl[t] = x_{t-1} (crossings of edge (t-1, t)), odd parity.
            # Node i constraint: x_{i-1} + x_i >= 2*c[i].
            xl = [0] * (n + 1)
            xl[0] = 1
            for i in range(n):
                v = 2 * c[i] - xl[i]
                if v < 1:
                    v = 1
                if v % 2 == 0:
                    v += 1
                xl[i + 1] = v
            # pref[t] = xl[0] + ... + xl[t-1]
            pref = [0] * (n + 2)
            for t in range(n + 1):
                pref[t + 1] = pref[t] + xl[t]

            # Right greedy: xr[j] = x_j for j in 0..n-2, even parity >= 2.
            # Node i (i >= 1) constraint: x_{i-1} + x_i >= 2*c[i], with x_{n-1} = 0.
            xr = [0] * (n + 1)
            nxt = 0
            for i in range(n - 1, 0, -1):
                v = 2 * c[i] - nxt
                if v < 2:
                    v = 2
                if v % 2 == 1:
                    v += 1
                xr[i - 1] = v
                nxt = v
            # sr[j] = xr[j] + ... + xr[n-2]
            sr = [0] * (n + 2)
            for j in range(n - 2, -1, -1):
                sr[j] = sr[j + 1] + xr[j]

            for e in range(n):
                Lsum = pref[e + 1]          # x_{-1} .. x_{e-1}
                Lx = xl[e]                  # x_{e-1}
                if e <= n - 2:
                    Rx = xr[e]              # x_e minimal given nodes e+1..n-1
                    Rsum = sr[e]            # x_e .. x_{n-2}
                else:
                    Rx = 0
                    Rsum = 0
                d = 2 * c[e] - 1 - Lx - Rx  # extra needed on x_e
                if d < 0:
                    d = 0
                if d % 2 == 1:
                    d += 1
                if Lsum + Rsum + d <= m:
                    return True
            return False

        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
