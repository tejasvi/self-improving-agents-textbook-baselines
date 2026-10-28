from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        parent = {}

        def find(x):
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        # Values > threshold can't form any edge (lcm >= value > threshold).
        small = [x for x in nums if x <= threshold]
        for x in nums:
            parent[x] = x
        components = len(nums)

        # For each v <= threshold, all nums-values dividing v are pairwise
        # connected (their lcm divides v, hence is <= threshold).
        divs = [[] for _ in range(threshold + 1)]
        for d in small:
            for m in range(d, threshold + 1, d):
                divs[m].append(d)

        for lst in divs:
            if len(lst) < 2:
                continue
            r0 = find(lst[0])
            for d in lst[1:]:
                r = find(d)
                if r != r0:
                    parent[r] = r0
                    components -= 1
        return components
