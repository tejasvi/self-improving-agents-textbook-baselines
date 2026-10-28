from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        small = [v for v in nums if v <= T]
        for v in nums:
            if v > T:
                parent[v] = v  # isolated node
        for v in small:
            parent[v] = v
        owner = [0] * (T + 1)  # 0 = unclaimed
        for v in small:
            for m in range(v, T + 1, v):
                o = owner[m]
                if o == 0:
                    owner[m] = v
                else:
                    a, b = find(v), find(o)
                    if a != b:
                        parent[a] = b
        return sum(1 for v in nums if find(v) == v)
