from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # a ~ b in graph iff lcm(a,b) <= threshold iff a and b both divide some L <= threshold.
        # DSU over 1..threshold: unite each num a (<= threshold) with all its multiples <= threshold.
        T = threshold
        parent = list(range(T + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        small = [a for a in nums if a <= T]
        isolated = len(nums) - len(small)
        for a in small:
            ra = find(a)
            for m in range(2 * a, T + 1, a):
                rm = find(m)
                if rm != ra:
                    parent[rm] = ra
        roots = {find(a) for a in small}
        return len(roots) + isolated
