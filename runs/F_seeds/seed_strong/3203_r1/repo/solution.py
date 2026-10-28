from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        m = n // 2
        # Pack 26 letter counts into one int: 18-bit fields (17 value bits + 1 guard bit).
        W = 18
        GUARD = 1 << 17
        G = 0
        for k in range(26):
            G |= GUARD << (W * k)
        ONE = [1 << (W * k) for k in range(26)]

        left = s[:m]
        t = s[m:][::-1]  # palindrome <=> left == t
        PS = [0] * (m + 1)
        PT = [0] * (m + 1)
        MP = [0] * (m + 1)
        acc_s = acc_t = acc_m = 0
        for i in range(m):
            cs = ord(left[i]) - 97
            ct = ord(t[i]) - 97
            acc_s += ONE[cs]
            acc_t += ONE[ct]
            if cs != ct:
                acc_m += 1
            PS[i + 1] = acc_s
            PT[i + 1] = acc_t
            MP[i + 1] = acc_m
        total_mis = acc_m
        if PS[m] != PT[m]:
            return [False] * len(queries)

        res = []
        for a, b, c, d in queries:
            # mirrored right segment in left-index coordinates
            c2 = n - 1 - d
            d2 = n - 1 - c
            # Mismatches must lie in U = [a,b] ∪ [c2,d2]
            lo = a if a > c2 else c2
            hi = b if b < d2 else d2
            inter = lo <= hi
            mis_u = (MP[b + 1] - MP[a]) + (MP[d2 + 1] - MP[c2])
            if inter:
                mis_u -= MP[hi + 1] - MP[lo]
            if mis_u != total_mis:
                res.append(False)
                continue
            S1 = PS[b + 1] - PS[a]
            T1 = PT[b + 1] - PT[a]
            S2 = PS[d2 + 1] - PS[c2]
            T2 = PT[d2 + 1] - PT[c2]
            if inter:
                Sx = PS[hi + 1] - PS[lo]
                Tx = PT[hi + 1] - PT[lo]
            else:
                Sx = Tx = 0
            # Letters of I1\I2 on t side must fit in S(I1); symmetric for I2.
            X1 = T1 - Tx  # t letters in I1 not in I2
            X2 = S2 - Sx  # s letters in I2 not in I1
            if ((((S1 | G) - X1) & G) != G) or ((((T2 | G) - X2) & G) != G):
                res.append(False)
                continue
            res.append(True)
        return res
