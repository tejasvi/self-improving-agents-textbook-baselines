from typing import *
from operator import sub, add


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        zero = (0,) * 26
        # prefix counts of s[0:h] (S) and of T where T[j] = s[n-1-j] (T)
        PS = [zero] * (h + 1)
        PT = [zero] * (h + 1)
        mp = [0] * (h + 1)
        cs = [0] * 26
        ct = [0] * 26
        m = 0
        for j in range(h):
            x = ord(s[j]) - 97
            y = ord(s[n - 1 - j]) - 97
            cs[x] += 1
            ct[y] += 1
            if x != y:
                m += 1
            PS[j + 1] = tuple(cs)
            PT[j + 1] = tuple(ct)
            mp[j + 1] = m
        total_mis = m
        res = []
        for a, b, c, d in queries:
            l1, r1 = a, b + 1
            l2, r2 = n - 1 - d, n - c
            li = max(l1, l2)
            ri = max(li, min(r1, r2))
            # every mismatch must lie inside L or R
            cov = (mp[r1] - mp[l1]) + (mp[r2] - mp[l2]) - (mp[ri] - mp[li])
            if cov != total_mis:
                res.append(False)
                continue
            sL = tuple(map(sub, PS[r1], PS[l1]))
            tL = tuple(map(sub, PT[r1], PT[l1]))
            sR = tuple(map(sub, PS[r2], PS[l2]))
            tR = tuple(map(sub, PT[r2], PT[l2]))
            tI = tuple(map(sub, PT[ri], PT[li]))
            sI = tuple(map(sub, PS[ri], PS[li]))
            AX = tuple(map(add, tuple(map(sub, sL, tL)), tI))
            BY = tuple(map(add, tuple(map(sub, tR, sR)), sI))
            res.append(AX == BY and min(AX) >= 0)
        return res
