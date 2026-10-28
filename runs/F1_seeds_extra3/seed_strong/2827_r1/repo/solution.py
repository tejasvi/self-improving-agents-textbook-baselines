from typing import *

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
        # nodes: 0..n-1 indices, n..n+MAX_V primes
        parent = list(range(n + MAX_V + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, v in enumerate(nums):
            if v == 1:
                return False
            x = v
            while x > 1:
                p = _spf[x]
                while x % p == 0:
                    x //= p
                a, b = find(i), find(n + p)
                if a != b:
                    parent[a] = b
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        return True
