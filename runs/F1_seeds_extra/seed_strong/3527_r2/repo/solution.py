from typing import *
from bisect import bisect_left, insort


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        col = list(colors)
        n = len(col)
        # Fenwick trees over run length T (tiles), storing count and sum of T.
        cnt_bit = [0] * (n + 1)
        sum_bit = [0] * (n + 1)
        total_cnt = [0]
        total_sum = [0]

        def upd(T, sign):
            # Add/remove one run of T tiles. Index reversed so suffix T>=k is a prefix.
            i = n - T + 1
            while i <= n:
                cnt_bit[i] += sign
                sum_bit[i] += sign * T
                i += i & -i

        def seg(a, b, sign):
            d = (b - a - 1) % n  # non-break edges between breaks a and b
            upd(d + 1, sign)

        breaks = []  # sorted break edge positions

        def is_break(e):
            return col[e] == col[(e + 1) % n]

        def insert(p):
            if not breaks:
                seg(p, p, 1)
            else:
                idx = bisect_left(breaks, p)
                a = breaks[idx - 1]  # idx-1 == -1 wraps to last element
                b = breaks[idx % len(breaks)]
                seg(a, b, -1)
                seg(a, p, 1)
                seg(p, b, 1)
            insort(breaks, p)

        def remove(p):
            breaks.pop(bisect_left(breaks, p))
            if not breaks:
                seg(p, p, -1)
            else:
                idx = bisect_left(breaks, p)
                a = breaks[idx - 1]
                b = breaks[idx % len(breaks)]
                seg(a, p, -1)
                seg(p, b, -1)
                seg(a, b, 1)

        for e in range(n):
            if is_break(e):
                insort(breaks, e)
        # build the trees from scratch
        if breaks:
            m = len(breaks)
            for j in range(m):
                seg(breaks[j], breaks[(j + 1) % m], 1)

        def query(k):
            # sum over runs with T>=k of (T-k+1)
            i = n - k + 1  # prefix up to reversed index for T>=k
            c = 0
            s = 0
            while i > 0:
                c += cnt_bit[i]
                s += sum_bit[i]
                i -= i & -i
            return s - (k - 1) * c

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if not breaks:
                    res.append(n)
                else:
                    res.append(query(k))
            else:
                _, idx, c = q
                if col[idx] == c:
                    continue
                edges = {(idx - 1) % n, idx}
                old = {e: is_break(e) for e in edges}
                col[idx] = c
                for e in edges:
                    nb = is_break(e)
                    if nb != old[e]:
                        if nb:
                            insert(e)
                        else:
                            remove(e)
        return res
