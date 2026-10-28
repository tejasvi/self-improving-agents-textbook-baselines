from typing import *


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        colors = list(colors)
        n = len(colors)
        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1

        # Fenwick over edge positions 0..n-1 (stored 1-indexed): bad-edge presence
        pos_tree = [0] * (n + 1)
        # Fenwick over run lengths 0..n-1 (stored at index len+1): count and sum of lengths
        cnt_tree = [0] * (n + 2)
        sum_tree = [0] * (n + 2)
        state = {'m': 0}

        def pos_add(i, d):
            i += 1
            while i <= n:
                pos_tree[i] += d
                i += i & -i

        def pos_prefix(i):  # count of bad in [0, i]
            i += 1
            s = 0
            while i > 0:
                s += pos_tree[i]
                i -= i & -i
            return s

        def pos_kth(k):  # 0-indexed position of k-th (1-based) bad edge
            p = 0
            rem = k
            step = 1 << LOG
            while step:
                np_ = p + step
                if np_ <= n and pos_tree[np_] < rem:
                    p = np_
                    rem -= pos_tree[np_]
                step >>= 1
            return p  # 1-indexed p+1 => 0-indexed p

        def run_add(length, d):
            i = length + 1
            while i <= n + 1:
                cnt_tree[i] += d
                sum_tree[i] += d * length
                i += i & -i

        def run_prefix(i):  # over lengths <= i-1 stored at index<=i ; returns (cnt, sum) for len < i
            c = 0
            s = 0
            while i > 0:
                c += cnt_tree[i]
                s += sum_tree[i]
                i -= i & -i
            return c, s

        def pred(e):  # largest bad position < e cyclically (e itself not bad or excluded)
            m = state['m']
            c = pos_prefix(e - 1) if e > 0 else 0
            if c == 0:
                return pos_kth(m)
            return pos_kth(c)

        def succ(e):  # smallest bad position > e cyclically
            m = state['m']
            c = pos_prefix(e)
            if c == m:
                return pos_kth(1)
            return pos_kth(c + 1)

        def gap(a, b):
            return (b - a - 1) % n

        def insert_bad(e):
            m = state['m']
            if m == 0:
                run_add(n - 1, 1)
            else:
                p = pred(e)
                q = succ(e)
                run_add(gap(p, q), -1)
                run_add(gap(p, e), 1)
                run_add(gap(e, q), 1)
            pos_add(e, 1)
            state['m'] = m + 1

        def remove_bad(e):
            m = state['m']
            pos_add(e, -1)
            state['m'] = m - 1
            if m == 1:
                run_add(n - 1, -1)
            else:
                p = pred(e)
                q = succ(e)
                run_add(gap(p, e), -1)
                run_add(gap(e, q), -1)
                run_add(gap(p, q), 1)

        bad = [False] * n
        for e in range(n):
            if colors[e] == colors[(e + 1) % n]:
                bad[e] = True
                insert_bad(e)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if state['m'] == 0:
                    res.append(n)
                    continue
                L = k - 1
                # sum over runs with len >= L of (len - L + 1)
                c_lt, s_lt = run_prefix(L)  # lengths < L
                c_all, s_all = run_prefix(n + 1)
                c = c_all - c_lt
                s = s_all - s_lt
                res.append(s - (L - 1) * c)
            else:
                idx, col = q[1], q[2]
                if colors[idx] == col:
                    continue
                colors[idx] = col
                for e in ((idx - 1) % n, idx):
                    nb = colors[e] == colors[(e + 1) % n]
                    if nb != bad[e]:
                        bad[e] = nb
                        if nb:
                            insert_bad(e)
                        else:
                            remove_bad(e)
        return res
