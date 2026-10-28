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

        # Values > threshold can't share an edge with anything: isolated.
        isolated = 0
        small = []
        for x in nums:
            if x > T:
                isolated += 1
            else:
                small.append(x)

        # x and y are adjacent iff lcm(x, y) <= T; lcm is a common multiple.
        # Union each small value with its multiples <= T.
        for x in small:
            for m in range(2 * x, T + 1, x):
                union(x, m)

        roots = {find(x) for x in small}
        return len(roots) + isolated
