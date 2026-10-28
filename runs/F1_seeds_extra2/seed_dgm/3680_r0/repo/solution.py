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

        small = [x for x in nums if x <= threshold]
        isolated = len(nums) - len(small)

        for x in small:
            for m in range(2 * x, threshold + 1, x):
                union(x, m)

        roots = {find(x) for x in small}
        return len(roots) + isolated
