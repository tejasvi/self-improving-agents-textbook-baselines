from typing import *
from operator import sub


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        m = n // 2
        L = [ord(ch) - 97 for ch in s[:m]]
        # R[i] = s[n-1-i]; palindrome <=> L[i] == R[i] for all i < m
        R = [ord(s[n - 1 - i]) - 97 for i in range(m)]

        # Prefix letter counts (tuples of 26) for L and R.
        PL = [(0,) * 26] * (m + 1)
        PR = [(0,) * 26] * (m + 1)
        cl = [0] * 26
        cr = [0] * 26
        PM = [0] * (m + 1)  # prefix count of mismatches
        for i in range(m):
            cl[L[i]] += 1
            cr[R[i]] += 1
            PL[i + 1] = tuple(cl)
            PR[i + 1] = tuple(cr)
            PM[i + 1] = PM[i] + (L[i] != R[i])
        total_mis = PM[m]
        global_ok = (PL[m] == PR[m])

        def cnt(P, l, r):
            # counts over inclusive [l, r] in index space (l <= r)
            return list(map(sub, P[r + 1], P[l]))

        res = []
        for a, b, c, d in queries:
            if not global_ok:
                res.append(False)
                continue
            bl, br = n - 1 - d, n - 1 - c  # mirror of [c, d] in left-index space
            lo, hi = max(a, bl), min(b, br)
            inter = lo <= hi
            inA = PM[b + 1] - PM[a]
            inB = PM[br + 1] - PM[bl]
            inI = (PM[hi + 1] - PM[lo]) if inter else 0
            if inA + inB - inI != total_mis:
                res.append(False)
                continue
            # Positions in A\B need R-values from pool L[A]; B\A need L-values from pool R[B].
            LA = cnt(PL, a, b)
            RB = cnt(PR, bl, br)
            RAmB = cnt(PR, a, b)
            LBmA = cnt(PL, bl, br)
            if inter:
                RAmB = list(map(sub, RAmB, cnt(PR, lo, hi)))
                LBmA = list(map(sub, LBmA, cnt(PL, lo, hi)))
            ok = all(x >= y for x, y in zip(LA, RAmB)) and \
                all(x >= y for x, y in zip(RB, LBmA))
            res.append(ok)
        return res
