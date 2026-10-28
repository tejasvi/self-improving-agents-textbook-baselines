from typing import *
from bisect import bisect_left


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        INF = n
        codes = [ord(ch) - 97 for ch in s]
        # fo[j][l] = first occurrence index of letter l at or after j (INF if none)
        fo = [None] * (n + 1)
        cur = [INF] * 27
        fo[n] = cur
        for j in range(n - 1, -1, -1):
            cur = cur[:]
            cur[codes[j]] = j
            fo[j] = cur
        sfo = [sorted(row) for row in fo]
        # f[j] = number of greedy partitions of s[j:] started fresh
        f = [0] * (n + 1)
        ej = [n] * (n + 1)
        for j in range(n - 1, -1, -1):
            e = sfo[j][k]  # (k+1)-th distinct first occurrence
            if e > n:
                e = n
            ej[j] = e
            f[j] = 1 + f[e]
        best = f[0]

        j = 0
        P = 0
        while j < n:
            e_seg = ej[j]
            inA = [False] * 26
            a = 0
            for i in range(j, e_seg):
                # letters in s[j:i] are inA; process change at i
                nxt = fo[i + 1]
                keys = [-1 if inA[l] else nxt[l] for l in range(26)] + [INF]
                X = sorted(keys)  # 27 entries; X[26] is sentinel INF
                sn = sfo[i + 1]
                for c in range(26):
                    if inA[c]:
                        q = X[k]
                    else:
                        p = bisect_left(X, nxt[c])
                        if k == a:
                            q = i
                        else:
                            q = X[k - 1] if k - 1 < p else X[k]
                    if q >= n:
                        tot = P + 1
                    elif q > i:
                        tot = P + 1 + f[q]
                    else:
                        # q == i, c not in A, k == a
                        p2 = bisect_left(sn, nxt[c])
                        w = sn[k - 1] if k - 1 < p2 else sn[k]
                        if w > n:
                            w = n
                        tot = P + 2 + f[w]
                    if tot > best:
                        best = tot
                codeI = codes[i]
                if not inA[codeI]:
                    inA[codeI] = True
                    a += 1
            P += 1
            j = e_seg
        return best
