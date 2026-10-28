from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        present = [False] * (T + 1)
        for x in nums:
            if x <= T:
                present[x] = True

        # divs[L] = present values dividing L (L <= T)
        divs = [[] for _ in range(T + 1)]
        for d in range(1, T + 1):
            if present[d]:
                for m in range(d, T + 1, d):
                    divs[m].append(d)

        parent = list(range(T + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = len(nums)
        for L in range(1, T + 1):
            ds = divs[L]
            if len(ds) < 2:
                continue
            r0 = find(ds[0])
            for d in ds[1:]:
                r = find(d)
                if r != r0:
                    parent[r] = r0
                    components -= 1
        return components
