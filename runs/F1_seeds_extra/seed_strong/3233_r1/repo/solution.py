from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # order[t]: letters sorted by first occurrence at index >= t (only those appearing)
        # fp[t][L]: first occurrence index of L at >= t (n if none)
        order = [None] * (n + 1)
        fp = [None] * (n + 1)
        order[n] = []
        fp[n] = [n] * 26
        for t in range(n - 1, -1, -1):
            L = a[t]
            nxt_fp = fp[t + 1][:]
            nxt_fp[L] = t
            fp[t] = nxt_fp
            order[t] = [L] + [x for x in order[t + 1] if x != L]

        def query(t, X, r):
            # first position p >= t where the r-th letter not in X (by first occurrence) appears;
            # n if there is no such letter.
            if r <= 0:
                return t
            cnt = 0
            for L in order[t]:
                if (X >> L) & 1:
                    continue
                cnt += 1
                if cnt == r:
                    return fp[t][L]
            return n

        # suf[t]: greedy partitions of s[t:] starting fresh at t (original string)
        suf = [0] * (n + 1)
        for t in range(n - 1, -1, -1):
            e = query(t, 0, k + 1)
            suf[t] = 1 + suf[e]
        best = suf[0]

        # Walk original greedy segmentation; for each i, know segment start b,
        # number of segments before b (P), and mask of s[b:i].
        b = 0
        mask = 0
        cnt_mask = 0
        P = 0
        for i in range(n):
            # current segment is s[b:i] with mask (distinct count = popcount(mask))
            for c in range(26):
                if (mask >> c) & 1:
                    X = mask
                else:
                    X = mask | (1 << c)
                d = bin(X).count("1")
                if d > k:
                    # segment [b, i) closes; s[i] (= c) starts new segment
                    e2 = query(i + 1, 1 << c, k)  # r = k - 1 + 1 = k
                    G = 1 + suf[e2]
                    total = P + 1 + G
                else:
                    e2 = query(i + 1, X, k - d + 1)
                    total = P + 1 + suf[e2]
                if total > best:
                    best = total
            # advance original greedy with s[i]
            bit = 1 << a[i]
            if (mask | bit).bit_count() > k:
                P += 1
                b = i
                mask = bit
            else:
                mask |= bit
        return best
