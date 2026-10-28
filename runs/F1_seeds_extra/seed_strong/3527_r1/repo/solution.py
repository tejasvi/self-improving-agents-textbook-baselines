from typing import *


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        col = list(colors)

        # Fenwick over bad-edge positions (0..n-1), 1-indexed internally
        pos_bit = [0] * (n + 1)
        # Fenwick over run lengths g (0..n-1): count and sum
        cnt_bit = [0] * (n + 1)
        sum_bit = [0] * (n + 1)
        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1
        state = {"total": 0}  # number of bad edges

        def pos_add(i, d):
            i += 1
            while i <= n:
                pos_bit[i] += d
                i += i & -i

        def pos_prefix(i):  # count of bad positions in [0, i]
            i += 1
            s = 0
            while i > 0:
                s += pos_bit[i]
                i -= i & -i
            return s

        def pos_kth(k):  # 0-indexed position of k-th (1-indexed) bad edge
            p = 0
            rem = k
            step = 1 << LOG
            while step:
                np_ = p + step
                if np_ <= n and pos_bit[np_] < rem:
                    p = np_
                    rem -= pos_bit[np_]
                step >>= 1
            return p  # 1-indexed p+1 -> 0-indexed p

        def gap_add(g, d):
            sd = d * g
            i = g + 1
            while i <= n:
                cnt_bit[i] += d
                sum_bit[i] += sd
                i += i & -i

        def gap_cnt_prefix(g):  # runs with length <= g
            i = g + 1
            s = 0
            while i > 0:
                s += cnt_bit[i]
                i -= i & -i
            return s

        def gap_sum_prefix(g):
            i = g + 1
            s = 0
            while i > 0:
                s += sum_bit[i]
                i -= i & -i
            return s

        def gap(x, y):
            return (y - x - 1) % n

        def insert(p):
            t = state["total"]
            if t == 0:
                gap_add(n - 1, 1)
            else:
                c = pos_prefix(p)  # bad positions <= p (p not yet inserted)
                if c > 0:
                    a = pos_kth(c)
                else:
                    a = pos_kth(t)
                if c < t:
                    b = pos_kth(c + 1)
                else:
                    b = pos_kth(1)
                gap_add(gap(a, b), -1)
                gap_add(gap(a, p), 1)
                gap_add(gap(p, b), 1)
            pos_add(p, 1)
            state["total"] = t + 1

        def remove(p):
            t = state["total"]
            pos_add(p, -1)
            t -= 1
            state["total"] = t
            if t == 0:
                gap_add(n - 1, -1)
            else:
                c = pos_prefix(p)  # includes p? p already removed, so count <= p excludes it
                # predecessor: largest bad < p
                if c > 0:
                    a = pos_kth(c)
                else:
                    a = pos_kth(t)
                # successor: smallest bad > p
                if c < t:
                    b = pos_kth(c + 1)
                else:
                    b = pos_kth(1)
                gap_add(gap(a, p), -1)
                gap_add(gap(p, b), -1)
                gap_add(gap(a, b), 1)

        def toggle_edge(e):
            # edge e between tile e and (e+1)%n
            f = (e + 1) % n
            bad = col[e] == col[f]
            return bad

        bad_now = [False] * n
        for e in range(n):
            if toggle_edge(e):
                bad_now[e] = True
                insert(e)

        res = []
        for q in queries:
            if q[0] == 1:
                s = q[1]
                if state["total"] == 0:
                    res.append(n)
                else:
                    k = s - 1  # need gap >= k
                    # sum over gaps g >= k of (g - (s-2)) ; runs with g<k excluded
                    totc = gap_cnt_prefix(n - 1)
                    tots = gap_sum_prefix(n - 1)
                    lc = gap_cnt_prefix(k - 1)
                    ls = gap_sum_prefix(k - 1)
                    cntG = totc - lc
                    sumG = tots - ls
                    res.append(sumG - (s - 2) * cntG)
            else:
                idx, c = q[1], q[2]
                if col[idx] == c:
                    continue
                col[idx] = c
                for e in ((idx - 1) % n, idx):
                    nb = toggle_edge(e)
                    if nb != bad_now[e]:
                        bad_now[e] = nb
                        if nb:
                            insert(e)
                        else:
                            remove(e)
        return res
