from typing import List


class Solution:
    _MAX = 100001
    _spf = None

    @classmethod
    def _build_spf(cls):
        if cls._spf is None:
            spf = list(range(cls._MAX))
            i = 2
            while i * i < cls._MAX:
                if spf[i] == i:
                    for j in range(i * i, cls._MAX, i):
                        if spf[j] == j:
                            spf[j] = i
                i += 1
            cls._spf = spf
        return cls._spf

    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        spf = self._build_spf()
        # Nodes 0..n-1 are indices; node n+p is prime p (p < MAX).
        parent = list(range(n + self._MAX))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i, v in enumerate(nums):
            if v == 1:
                return False
            x = v
            while x > 1:
                p = spf[x]
                union(i, n + p)
                while x % p == 0:
                    x //= p

        root = find(0)
        return all(find(i) == root for i in range(1, n))
