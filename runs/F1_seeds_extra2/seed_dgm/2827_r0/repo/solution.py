from typing import List

MAX_V = 100000
_spf = list(range(MAX_V + 1))
for _i in range(2, int(MAX_V ** 0.5) + 1):
    if _spf[_i] == _i:
        for _j in range(_i * _i, MAX_V + 1, _i):
            if _spf[_j] == _j:
                _spf[_j] = _i


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        # Nodes: indices 0..n-1, and prime p represented as n + p.
        parent = {}

        def find(x):
            parent.setdefault(x, x)
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i, v in enumerate(nums):
            if v == 1:
                return False  # isolated index while n > 1
            x = v
            while x > 1:
                p = _spf[x]
                union(i, n + p)
                while x % p == 0:
                    x //= p

        root0 = find(0)
        return all(find(i) == root0 for i in range(1, n))
