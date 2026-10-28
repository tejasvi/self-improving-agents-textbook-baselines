from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        present = set(x for x in nums if x <= T)
        # divs[L] = present values dividing L (L <= T)
        divs = [[] for _ in range(T + 1)]
        for d in present:
            for L in range(d, T + 1, d):
                divs[L].append(d)

        parent = {v: v for v in present}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for L in range(1, T + 1):
            lst = divs[L]
            if len(lst) > 1:
                r = find(lst[0])
                for v in lst[1:]:
                    rv = find(v)
                    if rv != r:
                        parent[rv] = r

        roots = set()
        for x in nums:
            if x <= T:
                roots.add(find(x))
            else:
                roots.add(('big', x))
        return len(roots)
