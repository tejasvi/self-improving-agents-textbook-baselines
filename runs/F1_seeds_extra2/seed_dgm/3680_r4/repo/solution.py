from typing import List


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

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        small = [x for x in nums if x <= T]
        isolated = len(nums) - len(small)

        # Connect each value x to all of its multiples up to threshold.
        for x in small:
            for m in range(2 * x, T + 1, x):
                union(x, m)

        roots = {find(x) for x in small}
        return isolated + len(roots)
