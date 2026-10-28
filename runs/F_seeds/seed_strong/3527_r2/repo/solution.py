from typing import *
from bisect import bisect_left, insort


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        colors = list(colors)
        n = len(colors)
        # Fenwick trees over run length (1..n): count and total length.
        cnt = [0] * (n + 1)
        sm = [0] * (n + 1)
        total_c = [0]
        total_s = [0]

        def upd(L, dc):
            # add run of length L with multiplicity dc (+1 / -1)
            total_c[0] += dc
            total_s[0] += dc * L
            i = L
            while i <= n:
                cnt[i] += dc
                sm[i] += dc * L
                i += i & (-i)

        def prefix(i):
            c = 0
            s = 0
            while i > 0:
                c += cnt[i]
                s += sm[i]
                i -= i & (-i)
            return c, s

        def gap(a, b):
            # length of run between bad edges a and b (circular), 1..n
            return ((b - a - 1) % n) + 1

        B = []  # sorted bad edge indices

        def is_bad(e):
            return colors[e] == colors[(e + 1) % n]

        for e in range(n):
            if is_bad(e):
                B.append(e)
        if not B:
            pass
        else:
            m = len(B)
            for j in range(m):
                upd(gap(B[j - 1], B[j]), 1)  # j-1 wraps to last when j==0

        def insert_edge(e):
            if not B:
                B.append(e)
                upd(n, 1)
                return
            i = bisect_left(B, e)
            p = B[i - 1] if i > 0 else B[-1]
            s = B[i] if i < len(B) else B[0]
            if len(B) == 1:
                # p == s, run of length n is split
                upd(n, -1)
            else:
                upd(gap(p, s), -1)
            upd(gap(p, e), 1)
            upd(gap(e, s), 1)
            B.insert(i, e)

        def remove_edge(e):
            i = bisect_left(B, e)
            del B[i]
            if not B:
                upd(n, -1)
                return
            p = B[i - 1] if i > 0 else B[-1]
            s = B[i] if i < len(B) else B[0]
            if len(B) == 1:
                # p == s
                upd(gap(p, e), -1)
                upd(gap(e, s), -1)
                upd(n, 1)
            else:
                upd(gap(p, e), -1)
                upd(gap(e, s), -1)
                upd(gap(p, s), 1)

        def toggle_check(e):
            bad_now = is_bad(e)
            i = bisect_left(B, e)
            in_set = i < len(B) and B[i] == e
            if bad_now and not in_set:
                insert_edge(e)
            elif not bad_now and in_set:
                remove_edge(e)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if not B:
                    res.append(n)
                else:
                    # sum over runs with L >= k of (L - k + 1)
                    c_low, s_low = prefix(k - 1)
                    c_ge = total_c[0] - c_low
                    s_ge = total_s[0] - s_low
                    res.append(s_ge - (k - 1) * c_ge)
            else:
                idx, col = q[1], q[2]
                colors[idx] = col
                toggle_check((idx - 1) % n)
                toggle_check(idx)
        return res
