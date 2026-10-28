from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        NEG = float('-inf')

        def feasible(x: int) -> bool:
            # c_i = visits needed at cell i
            c = [(x + p - 1) // p for p in points]
            # w0: need when walk passes cell once (base 1) ; w2: cells in [e, n-2] get base 2
            w0 = [ci - 1 if ci > 1 else 0 for ci in c]
            w2 = [ci - 2 if ci > 2 else 0 for ci in c]
            w2[n - 1] = w0[n - 1]
            # suffix G[i] = max weight independent set over cells i..n-1 using w2 (w0 for last)
            G = [0] * (n + 2)
            for i in range(n - 1, -1, -1):
                G[i] = max(G[i + 1], w2[i] + G[i + 2])
            # prefix over cells < e with w0; a0: last cell not taken, a1: last cell taken
            a0, a1 = 0, NEG
            for e in range(n):
                # walk ends at e
                mwis = max(a0 + G[e], a1 + G[e + 1])
                if 2 * n - 1 - e + 2 * mwis <= m:
                    return True
                # extend prefix with cell e (weight w0)
                a0, a1 = max(a0, a1), a0 + w0[e]
            return False

        lo, hi = 0, max(points) * (m + 1) + 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
