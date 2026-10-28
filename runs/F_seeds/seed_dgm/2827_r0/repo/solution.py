from typing import List

MAXV = 100000
_spf = list(range(MAXV + 1))
for _i in range(2, int(MAXV ** 0.5) + 1):
    if _spf[_i] == _i:
        for _j in range(_i * _i, MAXV + 1, _i):
            if _spf[_j] == _j:
                _spf[_j] = _i


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        parent = list(range(n + MAXV + 1))

        def find(x: int) -> int:
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
