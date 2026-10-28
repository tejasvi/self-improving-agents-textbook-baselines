from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        codes = [ord(ch) - 97 for ch in s]
        # L[q]: letters present in s[q:], sorted by first occurrence, as (pos, bit)
        L = [None] * (n + 1)
        L[n] = []
        first = [-1] * 26  # first occurrence position of each letter in s[q:]
        cur = []  # list of (pos, bit) maintained sorted by pos
        for q in range(n - 1, -1, -1):
            x = codes[q]
            # remove old entry of letter x, insert (q, bit) at front
            cur = [t for t in cur if t[1] != (1 << x)]
            cur.insert(0, (q, 1 << x))
            L[q] = cur

        def cut(q: int, S: int, size: int) -> int:
            """End (exclusive) of greedy segment starting at q with initial set S of given size."""
            r = k - size
            cnt = 0
            for pos, b in L[q]:
                if not (S & b):
                    if cnt == r:
                        return pos
                    cnt += 1
            return n

        # f[q] = greedy partition count of unchanged suffix s[q:]
        f = [0] * (n + 1)
        for q in range(n - 1, -1, -1):
            f[q] = 1 + f[cut(q, 0, 0)]
        best = f[0]

        a = 0
        j = 0
        while a < n:
            e = cut(a, 0, 0)
            P = 0
            psize = 0
            for i in range(a, e):
                # P = set of s[a:i]
                for c in range(26):
                    b = 1 << c
                    if P & b:
                        S = P
                        ssz = psize
                        if ssz <= k:
                            val = j + 1 + f[cut(i + 1, S, ssz)]
                            if val > best:
                                best = val
                    elif psize < k:
                        S = P | b
                        val = j + 1 + f[cut(i + 1, S, psize + 1)]
                        if val > best:
                            best = val
                    else:
                        # overflow at i: segment [a, i) closes, new segment starts at i with c
                        val = j + 2 + f[cut(i + 1, b, 1)]
                        if val > best:
                            best = val
                # extend prefix set with original s[i]
                b = 1 << codes[i]
                if not (P & b):
                    P |= b
                    psize += 1
            a = e
            j += 1
        return best
