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
        # Any 1 is isolated (gcd with anything is 1).
        if any(x == 1 for x in nums):
            return False

        # DSU over indices [0, n) and prime nodes [n, n + MAX).
        parent = list(range(n + _MAX))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, x in enumerate(nums):
            while x > 1:
                p = _spf[x]
                while x % p == 0:
                    x //= p
                a = find(i)
                b = find(n + p)
                if a != b:
                    parent[a] = b

        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        return True
