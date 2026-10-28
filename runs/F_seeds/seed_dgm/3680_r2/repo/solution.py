from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        t = threshold
        parent = list(range(t + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        # Values > threshold are isolated (lcm >= max(a, b) > threshold).
        small = [x for x in nums if x <= t]
        isolated = len(nums) - len(small)

        # a and b (both <= t) are connected iff lcm(a, b) <= t, iff they share
        # a multiple <= t. Union each value with its multiples <= t.
        for x in small:
            for m in range(2 * x, t + 1, x):
                union(x, m)

        roots = {find(x) for x in small}
        return len(roots) + isolated
