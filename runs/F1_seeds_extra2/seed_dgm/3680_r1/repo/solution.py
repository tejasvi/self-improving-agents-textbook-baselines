from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        parent = list(range(threshold + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        small = [v for v in nums if v <= threshold]
        # Two values a, b <= threshold are adjacent iff lcm(a, b) <= threshold,
        # i.e. both divide a common multiple <= threshold. Link each value to
        # all of its multiples within the threshold.
        for v in small:
            for m in range(2 * v, threshold + 1, v):
                union(v, m)

        roots = {find(v) for v in small}
        isolated = len(nums) - len(small)
        return len(roots) + isolated
