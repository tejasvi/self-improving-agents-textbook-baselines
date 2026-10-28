from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        NEG = -(1 << 62)

        def feasible(k: int) -> bool:
            if k == 0:
                return True
            # need[i]: visits required at index i.
            # Walk ending at e (e < n-1): base visits 1 for i < e, 2 for e <= i <= n-2,
            # 1 for i = n-1; cost of walk = 2n-1-e. Extra visits are bought by bounces
            # on edges (i, i+1) at 2 moves each; min bounces = max weight independent
            # set on the path with weights max(0, need - base).
            w1 = [0] * n  # weights with base 1
            w2 = [0] * n  # weights with base 2 (only used for indices <= n-2)
            for i in range(n):
                need = -(-k // points[i])
                w1[i] = need - 1 if need > 1 else 0
                if i < n - 1:
                    w2[i] = need - 2 if need > 2 else 0
                else:
                    w2[i] = w1[i]
            # Suffix DP over [e, n): S0[e] = best with e not taken, S1[e] = e taken.
            S0 = [0] * (n + 1)
            S1 = [NEG] * (n + 1)
            for e in range(n - 1, -1, -1):
                S0[e] = max(S0[e + 1], S1[e + 1])
                S1[e] = w2[e] + S0[e + 1]
            # Prefix DP over [0, e): Pn[e] = best with e-1 not taken, Pt[e] = e-1 taken.
            Pn = 0
            Pt = NEG
            for e in range(n):
                # end at e: prefix [0,e) uses w1, suffix [e,n) uses w2
                mw = max(Pn + max(S0[e], S1[e]), Pt + S0[e])
                cost = 2 * n - 1 - e + 2 * mw
                if cost <= m:
                    return True
                # advance prefix over index e
                Pn, Pt = max(Pn, Pt), w1[e] + Pn
            return False

        lo, hi = 0, 10 ** 15 + 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
