from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        t = threshold
        # Values above threshold can never join any edge (lcm >= value > t).
        isolated = 0
        present = []
        for v in nums:
            if v > t:
                isolated += 1
            else:
                present.append(v)

        # DSU over values (indexed by value, only values <= t are used).
        parent = list(range(t + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        # lcm(a, b) <= t  <=>  a and b both divide some L <= t (L = lcm(a, b)).
        # For each L, union all present divisors of L.
        rep = [0] * (t + 1)  # 0 means no divisor seen yet (values are >= 1)
        for d in present:
            for L in range(d, t + 1, d):
                r = rep[L]
                if r == 0:
                    rep[L] = d
                else:
                    a = find(d)
                    b = find(r)
                    if a != b:
                        parent[a] = b

        roots = set()
        for d in present:
            roots.add(find(d))
        return isolated + len(roots)
