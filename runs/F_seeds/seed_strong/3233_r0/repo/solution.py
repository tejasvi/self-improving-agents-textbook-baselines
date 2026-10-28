from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # Forward greedy state before each index i (original string).
        C = [0] * n      # completed segments before i
        Sm = [0] * n     # bitmask of open segment before i
        cnt = 0
        mask = 0
        d = 0
        for i in range(n):
            C[i] = cnt
            Sm[i] = mask
            b = 1 << a[i]
            if mask & b:
                continue
            if d < k:
                mask |= b
                d += 1
            else:
                cnt += 1
                mask = b
                d = 1

        # nxt[y]: end (exclusive) of the greedy segment starting fresh at y.
        nxt = [n] * (n + 1)
        occ = [0] * 26
        distinct = 0
        r = 0
        for y in range(n):
            if r < y:
                r = y
            while r < n and (distinct < k or occ[a[r]] > 0):
                if occ[a[r]] == 0:
                    distinct += 1
                occ[a[r]] += 1
                r += 1
            nxt[y] = r
            occ[a[y]] -= 1
            if occ[a[y]] == 0:
                distinct -= 1
        # f[y]: number of greedy segments of s[y:] starting fresh.
        f = [0] * (n + 1)
        for y in range(n - 1, -1, -1):
            f[y] = 1 + f[nxt[y]]

        best = f[0]

        # nextpos[L]: first occurrence of letter L at index >= i+1.
        nextpos = [n] * 26
        for i in range(n - 1, -1, -1):
            S = Sm[i]
            dd = bin(S).count("1")
            Ci = C[i]
            # letters sorted by first occurrence from i+1
            L0 = sorted(range(26), key=lambda L: nextpos[L])
            pos0 = [0] * 26
            for idx, L in enumerate(L0):
                pos0[L] = idx
            L1 = [L for L in L0 if not (S >> L) & 1]
            # yPos for L1 list
            def ypos(lst, j):
                if j < len(lst):
                    return nextpos[lst[j]]
                return n
            pos1 = {L: idx for idx, L in enumerate(L1)}
            for c in range(26):
                if (S >> c) & 1:
                    # case A, M = S
                    y = ypos(L1, k - dd)
                    total = Ci + 1 + f[y]
                elif dd < k:
                    # case A, M = S + {c}
                    j = k - dd - 1
                    p = pos1[c]
                    if j < p:
                        y = ypos(L1, j)
                    else:
                        y = ypos(L1, j + 1)
                    total = Ci + 1 + f[y]
                else:
                    # case B: c starts a new segment at i
                    j = k - 1
                    p0 = pos0[c]
                    if j < p0:
                        y = nextpos[L0[j]]
                    else:
                        y = nextpos[L0[j + 1]] if j + 1 < 26 else n
                    total = Ci + 2 + f[y]
                if total > best:
                    best = total
            nextpos[a[i]] = i
        return best
