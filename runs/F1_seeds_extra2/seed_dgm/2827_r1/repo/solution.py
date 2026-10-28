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
        if any(x == 1 for x in nums):
            return False

        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        first_idx = {}
        for i, x in enumerate(nums):
            while x > 1:
                p = _spf[x]
                while x % p == 0:
                    x //= p
                if p in first_idx:
                    a, b = find(i), find(first_idx[p])
                    if a != b:
                        parent[a] = b
                        components -= 1
                else:
                    first_idx[p] = i
        return components == 1
