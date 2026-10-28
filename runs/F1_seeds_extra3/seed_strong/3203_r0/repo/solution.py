from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        # Left part L[i] = s[i]; right part T[i] = s[n-1-i], for i in [0, h).
        # Rearrangeable: L over X=[a,b], T over Y=[n-1-d, n-1-c].
        # Fixed: L outside X, T outside Y.  Need L[i]==T[i] everywhere.
        pM = [0] * (h + 1)
        cL = [[0] * 26]
        cT = [[0] * 26]
        cur_L = [0] * 26
        cur_T = [0] * 26
        for i in range(h):
            x = ord(s[i]) - 97
            y = ord(s[n - 1 - i]) - 97
            cur_L[x] += 1
            cur_T[y] += 1
            pM[i + 1] = pM[i] + (x != y)
            cL.append(cur_L[:])
            cT.append(cur_T[:])
        total_mis = pM[h]
        if total_mis == 0:
            return [True] * len(queries)
        res = []
        for a, b, c, d in queries:
            x0, x1 = a, b + 1
            y0, y1 = n - 1 - d, n - c
            i0 = max(x0, y0)
            i1 = max(min(x1, y1), i0)
            cover = (pM[x1] - pM[x0]) + (pM[y1] - pM[y0]) - (pM[i1] - pM[i0])
            if cover != total_mis:
                res.append(False)
                continue
            Lx1, Lx0 = cL[x1], cL[x0]
            Ty1, Ty0 = cT[y1], cT[y0]
            Ti1, Ti0 = cT[i1], cT[i0]
            Li1, Li0 = cL[i1], cL[i0]
            ok = True
            for k in range(26):
                # R1[k] = L[X][k] - T[X\Y][k]
                r1 = (Lx1[k] - Lx0[k]) - ((cT[x1][k] - cT[x0][k]) - (Ti1[k] - Ti0[k]))
                if r1 < 0:
                    ok = False
                    break
                # R2[k] = T[Y][k] - L[Y\X][k]
                r2 = (Ty1[k] - Ty0[k]) - ((cL[y1][k] - cL[y0][k]) - (Li1[k] - Li0[k]))
                if r1 != r2:
                    ok = False
                    break
            res.append(ok)
        return res
