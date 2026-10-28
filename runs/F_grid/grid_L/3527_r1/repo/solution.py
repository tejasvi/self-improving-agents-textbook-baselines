from typing import List


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        colors = list(colors)

        # A "break" at position p means tile p and tile (p+1) % n have equal colors.
        # Breaks split the circle into maximal alternating runs. A run of length L
        # contributes max(0, L - k + 1) alternating groups of size k.
        # If there are no breaks, the whole circle is alternating: n groups for any k.

        pos_bit = [0] * (n + 1)  # Fenwick over break positions (1-indexed)
        cnt_bit = [0] * (n + 1)  # Fenwick over run lengths: count
        len_bit = [0] * (n + 1)  # Fenwick over run lengths: sum of lengths
        is_break = [False] * n

        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1

        def pos_add(i, v):
            i += 1
            while i <= n:
                pos_bit[i] += v
                i += i & -i

        def pos_prefix(i):  # number of breaks at positions <= i (0-indexed)
            i += 1
            s = 0
            while i > 0:
                s += pos_bit[i]
                i -= i & -i
            return s

        def pos_kth(k):  # k-th (1-indexed) break, returned as 0-indexed position
            p = 0
            for b in range(LOG, -1, -1):
                np_ = p + (1 << b)
                if np_ <= n and pos_bit[np_] < k:
                    p = np_
                    k -= pos_bit[np_]
            return p  # Fenwick index p+1 corresponds to 0-indexed position p

        def run_add(L, v):
            i = L
            while i <= n:
                cnt_bit[i] += v
                len_bit[i] += v * L
                i += i & -i

        def run_prefix(i):
            c = 0
            s = 0
            while i > 0:
                c += cnt_bit[i]
                s += len_bit[i]
                i -= i & -i
            return c, s

        def seglen(a, b):
            # length of the alternating run from break a to break b (cyclic)
            return (b - a - 1) % n + 1

        def add_break(p, m):
            # m = number of breaks before adding p
            if m == 0:
                run_add(n, 1)
            else:
                c = pos_prefix(p)  # breaks strictly before p
                a = pos_kth(c) if c > 0 else pos_kth(m)
                b = pos_kth(c + 1) if c < m else pos_kth(1)
                run_add(seglen(a, b), -1)
                run_add(seglen(a, p), 1)
                run_add(seglen(p, b), 1)
            pos_add(p, 1)

        def remove_break(p, m):
            # m = number of breaks before removing p
            pos_add(p, -1)
            if m == 1:
                run_add(n, -1)
                return
            c = pos_prefix(p)  # breaks strictly before p (p already removed)
            a = pos_kth(c) if c > 0 else pos_kth(m - 1)
            b = pos_kth(c + 1) if c < m - 1 else pos_kth(1)
            run_add(seglen(a, p), -1)
            run_add(seglen(p, b), -1)
            run_add(seglen(a, b), 1)

        m = 0
        for p in range(n):
            if colors[p] == colors[(p + 1) % n]:
                is_break[p] = True
                add_break(p, m)
                m += 1

        res = []
        for q in queries:
            if q[0] == 1:
                k = q[1]
                if m == 0:
                    res.append(n)
                    continue
                total_c, total_s = run_prefix(n)
                pc, ps = run_prefix(k - 1)
                # sum over runs L >= k of (L - k + 1)
                res.append((total_s - ps) - (k - 1) * (total_c - pc))
            else:
                idx, col = q[1], q[2]
                if colors[idx] == col:
                    continue
                colors[idx] = col
                for p in ((idx - 1) % n, idx):
                    want = colors[p] == colors[(p + 1) % n]
                    if want != is_break[p]:
                        is_break[p] = want
                        if want:
                            add_break(p, m)
                            m += 1
                        else:
                            remove_break(p, m)
                            m -= 1
        return res
