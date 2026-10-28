from typing import *


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        t = threshold
        parent = {}

        def find(x):
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        # Values > threshold are isolated (lcm with anything exceeds threshold).
        small = [x for x in nums if x <= t]
        isolated = len(nums) - len(small)
        for x in small:
            parent[x] = x
        # Two values are adjacent iff they share a common multiple m <= t
        # (lcm(a, b) is then <= m <= t). So for each m, union all nums that divide m.
        first = [0] * (t + 1)
        for x in small:
            for m in range(x, t + 1, x):
                f = first[m]
                if f == 0:
                    first[m] = x
                else:
                    rf, rx = find(f), find(x)
                    if rf != rx:
                        parent[rf] = rx
        roots = {find(x) for x in small}
        return isolated + len(roots)
