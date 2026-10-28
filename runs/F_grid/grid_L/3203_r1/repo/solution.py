from typing import List


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        h = n // 2
        # A[i] = s[i], T[i] = s[n-1-i] for i < h; palindrome <=> A == T.
        A = [ord(ch) - 97 for ch in s[:h]]
        T = [ord(ch) - 97 for ch in s[h:][::-1]]

        # prefix sums of mismatches
        mis = [0] * (h + 1)
        for i in range(h):
            mis[i + 1] = mis[i] + (A[i] != T[i])

        # per-letter prefix counts
        pa = [[0] * (h + 1) for _ in range(26)]
        pt = [[0] * (h + 1) for _ in range(26)]
        for i in range(h):
            for k in range(26):
                pa[k][i + 1] = pa[k][i]
                pt[k][i + 1] = pt[k][i]
            pa[A[i]][i + 1] += 1
            pt[T[i]][i + 1] += 1

        def cnt(p, l, r):
            # counts of letters in inclusive [l, r]; zeros if empty
            if l > r:
                return [0] * 26
            return [p[k][r + 1] - p[k][l] for k in range(26)]

        total_mis = mis[h]
        res = []
        for a, b, c, d in queries:
            x1, x2 = a, b
            y1, y2 = n - 1 - d, n - 1 - c  # mirrored Y range in A/T coordinates
            i1, i2 = max(x1, y1), min(x2, y2)
            has_i = i1 <= i2

            # mismatches inside X ∪ Y must cover all mismatches
            m_x = mis[x2 + 1] - mis[x1]
            m_y = mis[y2 + 1] - mis[y1]
            m_i = (mis[i2 + 1] - mis[i1]) if has_i else 0
            if total_mis != m_x + m_y - m_i:
                res.append(False)
                continue

            AX = cnt(pa, x1, x2)
            TX = cnt(pt, x1, x2)
            AY = cnt(pa, y1, y2)
            TY = cnt(pt, y1, y2)
            AI = cnt(pa, i1, i2) if has_i else [0] * 26
            TI = cnt(pt, i1, i2) if has_i else [0] * 26

            ok = True
            for k in range(26):
                # free pool in intersection, from X side
                v = AX[k] - (TX[k] - TI[k])
                if v < 0:
                    ok = False
                    break
                # from Y side
                if TY[k] - (AY[k] - AI[k]) != v:
                    ok = False
                    break
            res.append(ok)
        return res
