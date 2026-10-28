from typing import *
from bisect import bisect_left, insort


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        col = list(colors)

        # Fenwick trees over gap length g in [0, n-1] (index g+1): count and sum of g
        size = n + 1
        fc = [0] * (size + 1)
        fs = [0] * (size + 1)

        def upd(g, dc, ds):
            i = g + 1
            while i <= size:
                fc[i] += dc
                fs[i] += ds
                i += i & (-i)

        def pref(i):
            # returns (count, sum) over indices 1..i
            c = s = 0
            while i > 0:
                c += fc[i]
                s += fs[i]
                i -= i & (-i)
            return c, s

        total_cnt = [0]  # number of gaps
        bad = []  # sorted positions j where col[j] == col[(j+1)%n]

        def add_gap(g, sign):
            upd(g, sign, sign * g)
            total_cnt[0] += sign

        for j in range(n):
            if col[j] == col[(j + 1) % n]:
                bad.append(j)
        if bad:
            for idx in range(len(bad)):
                a = bad[idx]
                b = bad[(idx + 1) % len(bad)]
                add_gap((b - a - 1) % n, 1)

        def toggle(j, present):
            # present: True to insert j into bad set, False to remove
            m = len(bad)
            if present:
                if m == 0:
                    bad.append(j)
                    add_gap(n - 1, 1)
                    return
                pos = bisect_left(bad, j)
                p = bad[pos - 1] if pos > 0 else bad[-1]
                s = bad[pos] if pos < m else bad[0]
                # old gap (p -> s)
                add_gap((s - p - 1) % n, -1)
                add_gap((j - p - 1) % n, 1)
                add_gap((s - j - 1) % n, 1)
                bad.insert(pos, j)
            else:
                pos = bisect_left(bad, j)
                if m == 1:
                    bad.pop()
                    add_gap(n - 1, -1)
                    return
                p = bad[pos - 1] if pos > 0 else bad[-1]
                s = bad[pos + 1] if pos + 1 < m else bad[0]
                add_gap((j - p - 1) % n, -1)
                add_gap((s - j - 1) % n, -1)
                add_gap((s - p - 1) % n, 1)
                bad.pop(pos)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if not bad:
                    res.append(n)
                    continue
                # total over gaps with g >= k-1 : count and sum
                lo = k - 1  # index lo+1 is first with g >= lo ; prefix up to index lo
                c_all, s_all = pref(size)
                c_lo, s_lo = pref(lo)  # indices 1..lo correspond to g in [0, lo-1]
                cnt = c_all - c_lo
                sm = s_all - s_lo
                res.append(sm + (2 - k) * cnt)
            else:
                idx, c = q[1], q[2]
                if col[idx] == c:
                    continue
                col[idx] = c
                for j in ((idx - 1) % n, idx):
                    now = col[j] == col[(j + 1) % n]
                    pos = bisect_left(bad, j)
                    was = pos < len(bad) and bad[pos] == j
                    if now and not was:
                        toggle(j, True)
                    elif was and not now:
                        toggle(j, False)
        return res
