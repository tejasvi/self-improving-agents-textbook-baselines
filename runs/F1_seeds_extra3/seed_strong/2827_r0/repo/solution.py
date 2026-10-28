from typing import *


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False
        m = max(nums)
        spf = list(range(m + 1))
        i = 2
        while i * i <= m:
            if spf[i] == i:
                for j in range(i * i, m + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1
        parent = list(range(m + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        roots = []
        for v in nums:
            x = v
            p0 = spf[x]
            while x > 1:
                p = spf[x]
                ra, rb = find(p0), find(p)
                if ra != rb:
                    parent[ra] = rb
                while x % p == 0:
                    x //= p
            roots.append(p0)
        r0 = find(roots[0])
        for p0 in roots:
            if find(p0) != r0:
                return False
        return True
