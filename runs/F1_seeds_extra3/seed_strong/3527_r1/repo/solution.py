from typing import *


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        col = list(colors)
        # bad[e] = 1 if col[e] == col[(e+1)%n]  (edge between tile e and e+1)
        bad = [0] * n
        # Fenwick over bad positions (for pred/succ and k-th)
        pos = [0] * (n + 1)
        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1
        # Fenwick over gap lengths: index L+1 (L in [0, n-1])
        gcnt = [0] * (n + 2)
        gsum = [0] * (n + 2)
        m = n + 1  # size for gap fenwicks (indices 1..n+1)
        state = {"k": 0}

        def pos_add(i, d):
            i += 1
            while i <= n:
                pos[i] += d
                i += i & -i

        def pos_prefix(i):  # count of bad positions in [0, i-1]... i exclusive
            # returns number of set elements with index < i
            r = 0
            while i > 0:
                r += pos[i]
                i -= i & -i
            return r

        def pos_kth(k):  # 1-based k-th smallest set element index (0-based result)
            idx = 0
            bit = 1 << LOG
            while bit:
                nxt = idx + bit
                if nxt <= n and pos[nxt] < k:
                    idx = nxt
                    k -= pos[nxt]
                bit >>= 1
            return idx  # 1-based idx+1 -> 0-based idx

        def g_add(L, d):
            i = L + 1
            v = (L + 1) * d
            while i <= m:
                gcnt[i] += d
                gsum[i] += v
                i += i & -i

        def g_prefix(i):
            c = 0
            s = 0
            while i > 0:
                c += gcnt[i]
                s += gsum[i]
                i -= i & -i
            return c, s

        def gap(a, b):
            return (b - a - 1) % n

        def pred(p):
            total = state["k"]
            c = pos_prefix(p)  # number of set elements < p
            if c > 0:
                return pos_kth(c)
            return pos_kth(total)

        def succ(p):
            total = state["k"]
            c = pos_prefix(p + 1)  # number of set elements <= p
            if c < total:
                return pos_kth(c + 1)
            return pos_kth(1)

        def insert(p):
            k = state["k"]
            if k == 0:
                g_add(n - 1, 1)
            else:
                a = pred(p)
                b = succ(p)
                g_add(gap(a, b), -1)
                g_add(gap(a, p), 1)
                g_add(gap(p, b), 1)
            pos_add(p, 1)
            state["k"] = k + 1
            bad[p] = 1

        def remove(p):
            pos_add(p, -1)
            state["k"] -= 1
            bad[p] = 0
            k = state["k"]
            if k == 0:
                g_add(n - 1, -1)
            else:
                a = pred(p)
                b = succ(p)
                g_add(gap(a, p), -1)
                g_add(gap(p, b), -1)
                g_add(gap(a, b), 1)

        for e in range(n):
            if col[e] == col[(e + 1) % n]:
                insert(e)

        out = []
        for q in queries:
            if q[0] == 1:
                s = q[1]
                if state["k"] == 0:
                    out.append(n)
                    continue
                t = s - 1
                # gaps with L >= t
                c_all, s_all = g_prefix(m)
                c_lt, s_lt = g_prefix(t)  # gaps with L+1 <= t, i.e. L <= t-1
                cnt = c_all - c_lt
                sm = s_all - s_lt
                out.append(sm - t * cnt)
            else:
                i, c = q[1], q[2]
                if col[i] == c:
                    continue
                col[i] = c
                for e in ((i - 1) % n, i):
                    nb = 1 if col[e] == col[(e + 1) % n] else 0
                    if nb != bad[e]:
                        if nb:
                            insert(e)
                        else:
                            remove(e)
        return out
