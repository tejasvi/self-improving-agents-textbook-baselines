from typing import List


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        # rs[i] = s[n-1-i] for i in [0, half); palindrome <=> s[i] == rs[i] for all i < half.
        rs = s[::-1][:half]
        left = s[:half]

        # Prefix counts per letter for left (s) and rs.
        def build(t):
            pre = [[0] * (half + 1) for _ in range(26)]
            for c in range(26):
                ch = chr(97 + c)
                row = pre[c]
                acc = 0
                for i, x in enumerate(t):
                    if x == ch:
                        acc += 1
                    row[i + 1] = acc
            return pre

        ps = build(left)
        pr = build(rs)

        # Prefix count of mismatches between left and rs.
        mis = [0] * (half + 1)
        for i in range(half):
            mis[i + 1] = mis[i] + (left[i] != rs[i])
        total_mis = mis[half]

        def cnt(pre, l, r):
            # counts of letters in [l, r]; zero vector if empty
            if l > r:
                return [0] * 26
            return [pre[c][r + 1] - pre[c][l] for c in range(26)]

        def pieces_diff(x1, x2, y1, y2):
            # [x1,x2] minus [y1,y2] as list of intervals (inclusive)
            res = []
            if x1 > x2:
                return res
            if y1 > y2 or y2 < x1 or y1 > x2:
                return [(x1, x2)]
            if x1 < y1:
                res.append((x1, y1 - 1))
            if x2 > y2:
                res.append((y2 + 1, x2))
            return res

        def add(v, w):
            for c in range(26):
                v[c] += w[c]
            return v

        def sub(v, w):
            return [v[c] - w[c] for c in range(26)]

        ans = []
        for a, b, c, d in queries:
            a2, b2 = n - 1 - d, n - 1 - c  # right interval in rs coordinates
            # 1. All mismatches must lie inside A ∪ B.
            ia, ib = max(a, a2), min(b, b2)
            inter = mis[b + 1] - mis[a] + mis[b2 + 1] - mis[a2] - (
                (mis[ib + 1] - mis[ia]) if ia <= ib else 0)
            if inter != total_mis:
                ans.append(False)
                continue
            # 2. Multiset conditions.
            cs_A = cnt(ps, a, b)
            cr_B = cnt(pr, a2, b2)
            cr_P = [0] * 26
            for l, r in pieces_diff(a, b, a2, b2):
                add(cr_P, cnt(pr, l, r))
            cs_Q = [0] * 26
            for l, r in pieces_diff(a2, b2, a, b):
                add(cs_Q, cnt(ps, l, r))
            x = sub(cs_A, cr_P)
            y = sub(cr_B, cs_Q)
            ok = all(v >= 0 for v in x) and all(v >= 0 for v in y) and x == y
            ans.append(ok)
        return ans
