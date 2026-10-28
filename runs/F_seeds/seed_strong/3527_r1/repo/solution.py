from typing import *


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        col = list(colors)
        # Fenwick over edges e (between tile e and tile e+1 mod n): 1 if same color (break)
        ef = [0] * (n + 1)
        # Fenwick over run lengths: count and total length
        cf = [0] * (n + 1)
        lf = [0] * (n + 1)
        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1
        state = {'total': 0, 'cnt': 0, 'len': 0}

        def e_add(i, d):
            i += 1
            while i <= n:
                ef[i] += d
                i += i & -i

        def e_prefix(i):  # number of breaks in [0..i]
            i += 1
            s = 0
            while i > 0:
                s += ef[i]
                i -= i & -i
            return s

        def e_kth(j):  # index (0-based) of j-th smallest break, 1-based j
            pos = 0
            rem = j
            for b in range(LOG, -1, -1):
                np_ = pos + (1 << b)
                if np_ <= n and ef[np_] < rem:
                    pos = np_
                    rem -= ef[np_]
            return pos  # 1-based pos+1 -> 0-based pos

        def r_add(L, d):
            state['cnt'] += d
            state['len'] += d * L
            i = L
            while i <= n:
                cf[i] += d
                lf[i] += d * L
                i += i & -i

        def r_prefix(i):  # (count, length) for run lengths <= i
            c = 0
            s = 0
            while i > 0:
                c += cf[i]
                s += lf[i]
                i -= i & -i
            return c, s

        def pred(e):  # largest break < e (circular); assumes set nonempty
            c = e_prefix(e - 1) if e >= 1 else 0
            if c > 0:
                return e_kth(c)
            return e_kth(state['total'])

        def succ(e):  # smallest break > e (circular); assumes set nonempty
            c = e_prefix(e)
            if c < state['total']:
                return e_kth(c + 1)
            return e_kth(1)

        def insert(e):
            m = state['total']
            if m == 0:
                r_add(n, 1)
            else:
                p = pred(e)
                s = succ(e)
                if m == 1:
                    r_add(n, -1)
                else:
                    r_add((s - p) % n, -1)
                r_add((e - p) % n, 1)
                r_add((s - e) % n, 1)
            e_add(e, 1)
            state['total'] += 1

        def remove(e):
            e_add(e, -1)
            state['total'] -= 1
            m = state['total']
            if m == 0:
                r_add(n, -1)
            else:
                p = pred(e)
                s = succ(e)
                r_add((e - p) % n, -1)
                r_add((s - e) % n, -1)
                if m == 1:
                    r_add(n, 1)
                else:
                    r_add((s - p) % n, 1)

        def is_break(e):
            return col[e] == col[(e + 1) % n]

        brk = [False] * n
        for e in range(n):
            if is_break(e):
                brk[e] = True
                insert(e)

        def refresh(e):
            e %= n
            b = is_break(e)
            if b != brk[e]:
                brk[e] = b
                if b:
                    insert(e)
                else:
                    remove(e)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if state['total'] == 0:
                    res.append(n)
                else:
                    c, s = r_prefix(k - 1)
                    S0 = state['cnt'] - c
                    S1 = state['len'] - s
                    res.append(S1 - (k - 1) * S0)
            else:
                idx, c = q[1], q[2]
                if col[idx] != c:
                    col[idx] = c
                    refresh(idx - 1)
                    refresh(idx)
        return res
