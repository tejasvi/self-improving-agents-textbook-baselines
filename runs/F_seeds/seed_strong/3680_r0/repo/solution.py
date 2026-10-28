from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        parent = list(range(T + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        isolated = 0
        small = []
        for v in nums:
            if v > T:
                isolated += 1
            else:
                small.append(v)

        for v in small:
            m = 2 * v
            while m <= T:
                a, b = find(v), find(m)
                if a != b:
                    parent[a] = b
                m += v

        roots = {find(v) for v in small}
        return isolated + len(roots)
