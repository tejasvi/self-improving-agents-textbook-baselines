from typing import *


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
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        first_owner = {}
        for i, v in enumerate(nums):
            if v == 1:
                return False
            x = v
            while x > 1:
                p = _spf[x]
                while x % p == 0:
                    x //= p
                if p in first_owner:
                    a, b = find(i), find(first_owner[p])
                    if a != b:
                        parent[a] = b
                else:
                    first_owner[p] = i

        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        return True
