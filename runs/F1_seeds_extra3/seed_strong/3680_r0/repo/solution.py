from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                return True
            return False

        # Nums > threshold are isolated; they form their own components.
        small = [v for v in nums if v <= threshold]
        big_count = len(nums) - len(small)
        for v in small:
            parent[v] = v
        # anchor[L] = some num (<= threshold) dividing L, for L in 1..threshold
        anchor = [0] * (threshold + 1)
        components = len(small)
        for v in small:
            for L in range(v, threshold + 1, v):
                if anchor[L] == 0:
                    anchor[L] = v
                else:
                    if union(v, anchor[L]):
                        components -= 1
        return components + big_count
