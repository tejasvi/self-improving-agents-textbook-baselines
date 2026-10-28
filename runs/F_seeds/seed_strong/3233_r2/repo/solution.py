from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # Forward greedy: state before index i -> (cuts so far, open-segment letter mask)
        P = [0] * (n + 1)
        Mk = [0] * (n + 1)
        p = 0
        mask = 0
        cnt = 0
        for i in range(n):
            P[i] = p
            Mk[i] = mask
            b = 1 << a[i]
            if mask & b:
                pass
            elif cnt < k:
                mask |= b
                cnt += 1
            else:
                p += 1
                mask = b
                cnt = 1
        P[n] = p
        Mk[n] = mask
        base = p + 1  # no change option

        # Right-to-left: B = letters of s[i+1..] sorted by first occurrence,
        # fo[x] = first occurrence of x in s[i+1..] (or n if absent)
        INF = n
        fo = [INF] * 26
        B: List[int] = []
        suf = [0] * (n + 1)
        best = base

        def pick(Blist, excl, t, fo_arr):
            # t-th (0-indexed) element of Blist with letter excl removed; returns position or n
            if excl is None:
                if t < len(Blist):
                    return fo_arr[Blist[t]]
                return n
            idx = -1
            for q in range(len(Blist)):
                if Blist[q] == excl:
                    idx = q
                    break
            if idx == -1 or idx > t:
                if t < len(Blist):
                    return fo_arr[Blist[t]]
                return n
            if t + 1 < len(Blist):
                return fo_arr[Blist[t + 1]]
            return n

        for i in range(n - 1, -1, -1):
            c0 = a[i]
            # cut for segment starting at i with letter c: budget k-1 over B (letters after i)
            cut = [0] * 26
            for c in range(26):
                cut[c] = pick(B, c, k - 1, fo)
            suf[i] = 1 + suf[cut[c0]]

            M = Mk[i]
            pm = P[i]
            msz = bin(M).count("1")
            BM = [x for x in B if not (M >> x) & 1]
            for c in range(26):
                if (M >> c) & 1:
                    j1 = fo[BM[k - msz]] if k - msz < len(BM) else n
                    tot = pm + 1 + suf[j1]
                elif msz == k:
                    tot = pm + 2 + suf[cut[c]]
                else:
                    j1 = pick(BM, c, k - msz - 1, fo)
                    tot = pm + 1 + suf[j1]
                if tot > best:
                    best = tot

            # move: add position i to front
            fo[c0] = i
            B = [c0] + [x for x in B if x != c0]
        return best
