from typing import *
from bisect import bisect_left, insort


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        c = list(colors)
        n = len(c)
        # edge i connects tile i and tile (i+1)%n; it is a "break" if both colors equal.
        size = n + 1
        cnt_tree = [0] * (size + 1)
        sum_tree = [0] * (size + 1)
        total_cnt = [0]
        total_sum = [0]

        def upd(L, dc):
            # add run of length L with count change dc
            total_cnt[0] += dc
            total_sum[0] += dc * L
            i = L + 1
            while i <= size:
                cnt_tree[i] += dc
                sum_tree[i] += dc * L
                i += i & (-i)

        def prefix(L):
            # returns (count, sum) for run lengths <= L
            cc = 0
            ss = 0
            i = L + 1
            while i > 0:
                cc += cnt_tree[i]
                ss += sum_tree[i]
                i -= i & (-i)
            return cc, ss

        def gap(a, b):
            return (b - a - 1) % n

        breaks = []
        for i in range(n):
            if c[i] == c[(i + 1) % n]:
                breaks.append(i)
        if breaks:
            for j in range(len(breaks)):
                a = breaks[j]
                b = breaks[(j + 1) % len(breaks)]
                upd(gap(a, b), 1)

        def insert_break(x):
            if not breaks:
                breaks.append(x)
                upd(n - 1, 1)
                return
            m = len(breaks)
            idx = bisect_left(breaks, x)
            p = breaks[(idx - 1) % m]
            s = breaks[idx % m]
            upd(gap(p, s), -1)
            upd(gap(p, x), 1)
            upd(gap(x, s), 1)
            breaks.insert(idx, x)

        def remove_break(x):
            m = len(breaks)
            if m == 1:
                breaks.pop()
                upd(n - 1, -1)
                return
            idx = bisect_left(breaks, x)
            # breaks[idx] == x
            p = breaks[(idx - 1) % m]
            s = breaks[(idx + 1) % m]
            upd(gap(p, x), -1)
            upd(gap(x, s), -1)
            upd(gap(p, s), 1)
            breaks.pop(idx)

        def set_edge(e, is_break):
            idx = bisect_left(breaks, e)
            present = idx < len(breaks) and breaks[idx] == e
            if is_break and not present:
                insert_break(e)
            elif not is_break and present:
                remove_break(e)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if not breaks:
                    res.append(n)
                    continue
                # runs with L >= k-1 contribute (L - k + 2) each
                cc, ss = prefix(k - 2)
                cnt_ge = total_cnt[0] - cc
                sum_ge = total_sum[0] - ss
                res.append(sum_ge - (k - 2) * cnt_ge)
            else:
                idx, col = q[1], q[2]
                c[idx] = col
                for e in ((idx - 1) % n, idx):
                    set_edge(e, c[e] == c[(e + 1) % n])
        return res
