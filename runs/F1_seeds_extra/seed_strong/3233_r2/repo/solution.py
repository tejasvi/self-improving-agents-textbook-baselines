from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # Left pass: state before position i of the unchanged greedy.
        # cntB[i]: completed segments before the open segment; maskB[i]: open segment letters.
        cntB = [0] * n
        maskB = [0] * n
        cnt = 0
        mask = 0
        sz = 0
        for i in range(n):
            cntB[i] = cnt
            maskB[i] = mask
            bit = 1 << a[i]
            if not (mask & bit) and sz == k:
                cnt += 1
                mask = bit
                sz = 1
            else:
                if not (mask & bit):
                    mask |= bit
                    sz += 1

        INF = n  # absent letters -> segment reaches end
        f = [0] * (n + 1)  # f[x]: greedy partitions of s[x:] fresh start
        fo = [INF] * 26    # first occurrence positions > i
        best = 0

        def kth_excl(vals, idx, t):
            # value of the t-th (0-based) smallest among list excluding entry at idx
            if t < idx:
                v = vals[t]
            else:
                v = vals[t + 1] if t + 1 < 26 else INF
            return v

        for i in range(n - 1, -1, -1):
            order = sorted(range(26), key=fo.__getitem__)
            vals = [fo[x] for x in order]
            idxB = [0] * 26
            for p, x in enumerate(order):
                idxB[x] = p

            c0 = a[i]
            e2 = kth_excl(vals, idxB[c0], k - 1)
            if e2 > n:
                e2 = n
            f[i] = 1 + f[e2]

            M = maskB[i]
            cn = cntB[i]
            sz = bin(M).count("1")
            # A = letters not in M, sorted by fo
            A = [x for x in order if not (M >> x) & 1]
            lenA = len(A)
            Avals = [fo[x] for x in A]
            idxA = [-1] * 26
            for p, x in enumerate(A):
                idxA[x] = p
            for c in range(26):
                if (M >> c) & 1:
                    t = k - sz
                    e = Avals[t] if t < lenA else INF
                    tot = cn + 1 + f[e]
                elif sz < k:
                    t = k - sz - 1
                    e = kth_excl(Avals, idxA[c], t) if t < lenA - 1 else INF
                    if e > n:
                        e = INF
                    tot = cn + 1 + f[e]
                else:
                    e2c = kth_excl(vals, idxB[c], k - 1)
                    if e2c > n:
                        e2c = n
                    tot = cn + 2 + f[e2c]
                if tot > best:
                    best = tot
            fo[c0] = i
        if f[0] > best:
            best = f[0]
        return best
