from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        SH = 18  # counts <= 1e5 < 2^17; differences fit in (-2^17, 2^17) so packing is unique
        MASK = (1 << SH) - 1
        # packed prefix counts: P[i] = sum over s[:i] of 1 << (SH * letter)
        P = [0] * (n + 1)
        cur = 0
        for i, ch in enumerate(s):
            cur += 1 << (SH * (ord(ch) - 97))
            P[i + 1] = cur
        # mismatch prefix over left-half pairs
        mis = [0] * (h + 1)
        for i in range(h):
            mis[i + 1] = mis[i] + (1 if s[i] != s[n - 1 - i] else 0)
        total_bad = mis[h]

        def cnt(lo, hi):  # packed counts over absolute [lo, hi]; empty if lo > hi
            if lo > hi:
                return 0
            return P[hi + 1] - P[lo]

        def bad(lo, hi):
            if lo > hi:
                return 0
            return mis[hi + 1] - mis[lo]

        def inter(l1, h1, l2, h2):
            return max(l1, l2), min(h1, h2)

        res = []
        for a, b, c, d in queries:
            Al, Ah = a, b
            Ml, Mh = n - 1 - d, n - 1 - c
            Bl, Bh = c, d
            mAl, mAh = n - 1 - b, n - 1 - a
            AMl, AMh = inter(Al, Ah, Ml, Mh)
            if total_bad - bad(Al, Ah) - bad(Ml, Mh) + bad(AMl, AMh) != 0:
                res.append(False)
                continue
            mABl, mABh = inter(mAl, mAh, Bl, Bh)
            X = cnt(Al, Ah) - (cnt(mAl, mAh) - cnt(mABl, mABh))
            Y = cnt(Bl, Bh) - (cnt(Ml, Mh) - cnt(AMl, AMh))
            if X != Y:
                res.append(False)
                continue
            # X is the true count vector (with each digit) only if all digits >= 0
            ok = True
            x = X
            # Extract signed digits in base 2^SH; a negative digit means a borrow.
            # Compute the true digit sequence and check all >= 0.
            for _ in range(26):
                dgt = x & MASK
                if dgt >= (1 << (SH - 1)):
                    dgt -= 1 << SH
                if dgt < 0:
                    ok = False
                    break
                x = (x - dgt) >> SH
            res.append(ok)
        return res
