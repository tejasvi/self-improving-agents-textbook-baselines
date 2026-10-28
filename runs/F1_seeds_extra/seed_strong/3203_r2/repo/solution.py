from typing import *


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        m = n // 2
        L = s[:m]
        R = s[m:][::-1]  # R[i] = s[n-1-i]
        K = 1 << 17  # > any letter count (<= 5*10^4); balanced encoding is exact
        W = [K ** c for c in range(26)]

        # prefix sums (base-K encoded) of F = L - R, mismatch counts, and per-letter counts
        PF = [0] * (m + 1)
        PM = [0] * (m + 1)
        PL = [[0] * (m + 1) for _ in range(26)]
        PR = [[0] * (m + 1) for _ in range(26)]
        acc = 0
        mis = 0
        for i in range(m):
            x = ord(L[i]) - 97
            y = ord(R[i]) - 97
            acc += W[x] - W[y]
            PF[i + 1] = acc
            if x != y:
                mis += 1
            PM[i + 1] = mis
            for c in range(26):
                PL[c][i + 1] = PL[c][i]
                PR[c][i + 1] = PR[c][i]
            PL[x][i + 1] += 1
            PR[y][i + 1] += 1
        total = mis

        res = []
        for a, b, c, d in queries:
            alo, ahi = a, b + 1                 # left interval, half-open
            blo, bhi = n - 1 - d, n - c         # mirrored right interval, half-open
            ilo = max(alo, blo)
            ihi = min(ahi, bhi)
            if ilo >= ihi:
                ihi = ilo  # empty intersection
            # all mismatches must lie in A ∪ B
            cov = (PM[ahi] - PM[alo]) + (PM[bhi] - PM[blo]) - (PM[ihi] - PM[ilo])
            if cov != total:
                res.append(False)
                continue
            # multiset of L over A∪B must equal multiset of R over A∪B
            if PF[ahi] - PF[alo] + PF[bhi] - PF[blo] - (PF[ihi] - PF[ilo]) != 0:
                res.append(False)
                continue
            # positions of A\B have fixed right values R[A\B]; they must be provided by L[A]
            ok = True
            for ch in range(26):
                P_L = PL[ch]
                P_R = PR[ch]
                if P_L[ahi] - P_L[alo] - (P_R[ahi] - P_R[alo]) + (P_R[ihi] - P_R[ilo]) < 0:
                    ok = False
                    break
            res.append(ok)
        return res
