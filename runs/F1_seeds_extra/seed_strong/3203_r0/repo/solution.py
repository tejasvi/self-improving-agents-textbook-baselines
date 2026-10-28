from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        SH = 18          # bits per letter field (counts < 2^17)
        HALF = 1 << 17
        # A[j] = s[j], B[j] = s[n-1-j] for j in [0, h)
        A = [ord(ch) - 97 for ch in s[:h]]
        B = [ord(s[n - 1 - j]) - 97 for j in range(h)]

        # Global balance: multisets of A and B must be equal.
        cnt = [0] * 26
        for x in A:
            cnt[x] += 1
        for x in B:
            cnt[x] -= 1
        balanced = all(v == 0 for v in cnt)

        # Packed prefix sums of letter counts for A and B.
        PA = [0] * (h + 1)
        PB = [0] * (h + 1)
        acc_a = 0
        acc_b = 0
        for j in range(h):
            acc_a += 1 << (SH * A[j])
            acc_b += 1 << (SH * B[j])
            PA[j + 1] = acc_a
            PB[j + 1] = acc_b

        # Prefix sums of mismatches.
        pre = [0] * (h + 1)
        for j in range(h):
            pre[j + 1] = pre[j] + (A[j] != B[j])

        GUARD = 0
        GM = 0
        for k in range(26):
            GUARD += HALF << (SH * k)
            GM += (1 << (SH * k + 17))

        def mism(l, r):  # inclusive
            if l > r:
                return 0
            return pre[r + 1] - pre[l]

        res = []
        for a, b, c, d in queries:
            if not balanced:
                res.append(False)
                continue
            # right query [c, d] in s maps to B-index range [c2, d2]
            c2, d2 = n - 1 - d, n - 1 - c
            lo = max(a, c2)
            hi = min(b, d2)
            inter = mism(lo, hi) if lo <= hi else 0
            covered = mism(a, b) + mism(c2, d2) - inter
            if covered != pre[h]:
                res.append(False)
                continue
            # Per-letter feasibility: B[Q2'] - A[Q2'] + A[I] >= 0
            D = PB[d2 + 1] - PB[c2] - (PA[d2 + 1] - PA[c2])
            if lo <= hi:
                D += PA[hi + 1] - PA[lo]
            X = D + GUARD
            res.append((X & GM) == GM)
        return res
