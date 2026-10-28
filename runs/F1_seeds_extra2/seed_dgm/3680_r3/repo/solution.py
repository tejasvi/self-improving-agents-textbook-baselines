from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        parent = list(range(threshold + 1))

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

        # Values above threshold are isolated; values <= threshold connect
        # to every multiple <= threshold (two values are adjacent iff they
        # share a common multiple <= threshold, i.e. lcm <= threshold).
        small = [x for x in nums if x <= threshold]
        isolated = len(nums) - len(small)
        for x in small:
            m = x
            while m <= threshold:
                union(x, m)
                m += x

        roots = {find(x) for x in small}
        return len(roots) + isolated
