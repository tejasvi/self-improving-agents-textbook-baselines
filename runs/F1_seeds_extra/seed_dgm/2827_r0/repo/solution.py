from typing import List


_MAX = 100001
_spf = list(range(_MAX))
for _i in range(2, int(_MAX ** 0.5) + 1):
    if _spf[_i] == _i:
        for _j in range(_i * _i, _MAX, _i):
            if _spf[_j] == _j:
                _spf[_j] = _i


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        # Nodes 0..n-1 are indices; n + p is the prime p (only primes up to 1e5 used).
        parent = list(range(n + _MAX))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, v in enumerate(nums):
            if v == 1:
                return False
            while v > 1:
                p = _spf[v]
                while v % p == 0:
                    v //= p
                a, b = find(i), find(n + p)
                if a != b:
                    parent[a] = b

        root = find(0)
        return all(find(i) == root for i in range(n))
