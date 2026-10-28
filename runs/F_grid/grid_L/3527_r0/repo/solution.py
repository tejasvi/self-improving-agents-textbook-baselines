from typing import List


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        col = list(colors)

        # Fenwick over edge positions 0..n-1 (edge e connects tile e and tile e+1 mod n)
        pos_tree = [0] * (n + 1)
        # Fenwick over reversed run lengths: index r = n+1-L (L in 1..n)
        cnt_tree = [0] * (n + 1)
        sum_tree = [0] * (n + 1)
        bad = [False] * n
        state = {"total": 0}

        def pos_add(i, v):
            i += 1
            while i <= n:
                pos_tree[i] += v
                i += i & -i

        def pos_prefix(i):  # count of bad edges with index <= i (i may be -1)
            i += 1
            s = 0
            while i > 0:
                s += pos_tree[i]
                i -= i & -i
            return s

        def pos_kth(k):  # 1-based k-th bad edge, returns index
            idx = 0
            step = 1
            while step * 2 <= n:
                step *= 2
            while step:
                nxt = idx + step
                if nxt <= n and pos_tree[nxt] < k:
                    idx = nxt
                    k -= pos_tree[nxt]
                step //= 2
            return idx  # 0-based index of the element

        def run_add(L, v):
            r = n + 1 - L
            while r <= n:
                cnt_tree[r] += v
                sum_tree[r] += v * L
                r += r & -r

        def dist(a, b):
            if a == b:
                return n
            return (b - a) % n

        def pred(e):  # largest bad edge < e cyclically (e itself excluded)
            c = pos_prefix(e - 1)
            if c > 0:
                return pos_kth(c)
            return pos_kth(state["total"])

        def succ(e):  # smallest bad edge > e cyclically
            c = pos_prefix(e)
            if c < state["total"]:
                return pos_kth(c + 1)
            return pos_kth(1)

        def add_edge(e):
            if state["total"] == 0:
                run_add(n, 1)
            else:
                p = pred(e)
                q = succ(e)
                run_add(dist(p, q), -1)
                run_add(dist(p, e), 1)
                run_add(dist(e, q), 1)
            pos_add(e, 1)
            state["total"] += 1
            bad[e] = True

        def remove_edge(e):
            pos_add(e, -1)
            state["total"] -= 1
            bad[e] = False
            if state["total"] == 0:
                run_add(n, -1)
            else:
                p = pred(e)
                q = succ(e)
                run_add(dist(p, e), -1)
                run_add(dist(e, q), -1)
                run_add(dist(p, q), 1)

        def suffix_stats(k):
            # sum over runs with L >= k of L, and count
            r = n + 1 - k
            c = 0
            s = 0
            while r > 0:
                c += cnt_tree[r]
                s += sum_tree[r]
                r -= r & -r
            return c, s

        for e in range(n):
            if col[e] == col[(e + 1) % n]:
                add_edge(e)

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if state["total"] == 0:
                    res.append(n)
                else:
                    c, s = suffix_stats(k)
                    res.append(s - (k - 1) * c)
            else:
                idx, color = q[1], q[2]
                for e in ((idx - 1) % n, idx):
                    if bad[e]:
                        remove_edge(e)
                col[idx] = color
                for e in ((idx - 1) % n, idx):
                    if col[e] == col[(e + 1) % n]:
                        add_edge(e)
        return res
