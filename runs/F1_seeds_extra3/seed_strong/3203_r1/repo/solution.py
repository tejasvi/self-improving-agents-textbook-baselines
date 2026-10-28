from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        W = 17          # field width in bits (counts < 2^16)
        HB = 1 << 16    # high bit inside each field
        NF = 26
        H = 0
        G = 0
        for c in range(NF):
            H |= HB << (W * c)
        G = H

        # Left half L[i] = s[i]; right-side mirrored X[i] = s[n-1-i], i in [0, h)
        mis = [0] * (h + 1)
        EL = [0] * (h + 1)   # packed prefix counts of L
        EX = [0] * (h + 1)   # packed prefix counts of X
        for i in range(h):
            l = s[i]
            x = s[n - 1 - i]
            mis[i + 1] = mis[i] + (l != x)
            EL[i + 1] = EL[i] + (1 << (W * (ord(l) - 97)))
            EX[i + 1] = EX[i] + (1 << (W * (ord(x) - 97)))
        total_mis = mis[h]

        res = []
        for a, b, c, d in queries:
            lo = n - 1 - d
            hi = n - 1 - c
            # all mismatches must lie in P ∪ Q
            ia = a if a > lo else lo
            ib = b if b < hi else hi
            if ia <= ib:
                mi = mis[ib + 1] - mis[ia]
                LI = EL[ib + 1] - EL[ia]
                XI = EX[ib + 1] - EX[ia]
            else:
                mi = 0
                LI = 0
                XI = 0
            m = (mis[b + 1] - mis[a]) + (mis[hi + 1] - mis[lo]) - mi
            if m != total_mis:
                res.append(False)
                continue
            LP = EL[b + 1] - EL[a]
            XP = EX[b + 1] - EX[a]
            LQ = EL[hi + 1] - EL[lo]
            XQ = EX[hi + 1] - EX[lo]
            # balance on P ∪ Q
            if LP + LQ - LI != XP + XQ - XI:
                res.append(False)
                continue
            # X on P\I must fit into L on P
            XA = XP - XI
            if ((LP + G - XA) & H) != H:
                res.append(False)
                continue
            # L on Q\I must fit into X on Q
            LB = LQ - LI
            if ((XQ + G - LB) & H) != H:
                res.append(False)
                continue
            res.append(True)
        return res
