from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        parent = list(range(T + 1))

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        small = []
        isolated = 0
        for x in nums:
            if x > T:
                isolated += 1
            else:
                small.append(x)

        # owner[m] = some present value dividing m (among those processed)
        owner = [0] * (T + 1)
        for x in small:
            for m in range(x, T + 1, x):
                o = owner[m]
                if o == 0:
                    owner[m] = x
                else:
                    rx, ro = find(x), find(o)
                    if rx != ro:
                        parent[rx] = ro

        roots = set(find(x) for x in small)
        return isolated + len(roots)
