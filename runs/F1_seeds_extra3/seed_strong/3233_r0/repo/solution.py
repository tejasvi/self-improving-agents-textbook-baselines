from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # end[p]: first index q >= p such that a[p..q] has > k distinct (n if none)
        end = [n] * (n + 1)
        cnt = [0] * 26
        distinct = 0
        q = 0
        for p in range(n):
            while q < n:
                x = a[q]
                if cnt[x] == 0:
                    if distinct == k:
                        break
                    distinct += 1
                cnt[x] += 1
                q += 1
            end[p] = q
            x = a[p]
            cnt[x] -= 1
            if cnt[x] == 0:
                distinct -= 1

        # f[p]: greedy partition count of original suffix starting at p
        f = [0] * (n + 1)
        for p in range(n - 1, -1, -1):
            f[p] = 1 + f[end[p]]
        best = f[0]

        # original greedy segments: segidx[i], B[i] = letter mask of segment prefix before i
        segidx = [0] * n
        B = [0] * n
        st = 0
        idx = 0
        while st < n:
            en = end[st]
            mask = 0
            for i in range(st, en):
                B[i] = mask
                mask |= 1 << a[i]
                segidx[i] = idx
            idx += 1
            st = en

        # order: letters present at positions >= p, sorted by next occurrence
        npos = [n] * 26
        order: List[int] = []  # letters, ascending by npos
        for i in range(n - 1, -1, -1):
            # state corresponds to positions >= i+1
            Bm = B[i]
            bsz = bin(Bm).count("1")
            mi = segidx[i]
            # L: letters not in B, with positions, ascending
            Lpos = []
            Lidx = [-1] * 26  # index of letter within L
            for x in order:
                if not (Bm >> x) & 1:
                    Lidx[x] = len(Lpos)
                    Lpos.append(npos[x])
            Fpos = [npos[x] for x in order]
            Fidx = [-1] * 26
            for t, x in enumerate(order):
                Fidx[x] = t
            lenL = len(Lpos)
            lenF = len(Fpos)

            for c in range(26):
                if (Bm >> c) & 1:
                    m = k + 1 - bsz  # need m new letters from L (c is in B, not removed)
                    if m <= lenL:
                        e = Lpos[m - 1]
                    else:
                        e = n
                    cand = mi + 1 + f[e]
                else:
                    if bsz == k:
                        # case A: cut at i; new segment starts at i with letter c
                        # need k letters != c from positions >= i+1 in full order
                        t = Fidx[c]
                        m = k
                        if t == -1 or t >= m:
                            pass
                        else:
                            m = k + 1
                        if m <= lenF:
                            # m-th element excluding c
                            # if c among first k, we need the (k+1)-th
                            e = Fpos[m - 1]
                        else:
                            e = n
                        cand = mi + 2 + f[e]
                    else:
                        m = k - bsz  # m >= 1
                        t = Lidx[c]
                        if t == -1 or t >= m:
                            mm = m
                        else:
                            mm = m + 1
                        if mm <= lenL:
                            e = Lpos[mm - 1]
                        else:
                            e = n
                        cand = mi + 1 + f[e]
                if cand > best:
                    best = cand

            # add s[i] to front of order
            x = a[i]
            if x in order:
                order.remove(x)
            order.insert(0, x)
            npos[x] = i
        return best
