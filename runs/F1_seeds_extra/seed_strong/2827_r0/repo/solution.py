from typing import *


class Solution:
    _spf = None

    @classmethod
    def _build_spf(cls, limit):
        if cls._spf is None or len(cls._spf) <= limit:
            spf = list(range(limit + 1))
            i = 2
            while i * i <= limit:
                if spf[i] == i:
                    for j in range(i * i, limit + 1, i):
                        if spf[j] == j:
                            spf[j] = i
                i += 1
            cls._spf = spf
        return cls._spf

    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False
        spf = self._build_spf(max(nums))
        # DSU over nodes: 0..n-1 for indices, n + p for prime p.
        parent = list(range(n + max(nums) + 1))

        def find(x):
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        for i, v in enumerate(nums):
            x = v
            while x > 1:
                p = spf[x]
                while x % p == 0:
                    x //= p
                a = find(i)
                b = find(n + p)
                if a != b:
                    parent[a] = b
        root0 = find(0)
        return all(find(i) == root0 for i in range(n))
