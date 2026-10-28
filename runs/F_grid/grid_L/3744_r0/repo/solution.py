from typing import List


class Solution:
    @staticmethod
    def _F(n: int) -> int:
        # sum of base-4 digit lengths of x for x in [1, n]
        total = 0
        k = 1
        lo = 1  # 4^(k-1)
        while lo <= n:
            hi = min(n, 4 * lo - 1)
            total += (hi - lo + 1) * k
            lo *= 4
            k += 1
        return total

    @staticmethod
    def _f(x: int) -> int:
        k = 0
        while x:
            x >>= 2
            k += 1
        return k

    def minOperations(self, queries: List[List[int]]) -> int:
        res = 0
        for l, r in queries:
            s = self._F(r) - self._F(l - 1)
            res += max(self._f(l), (s + 1) // 2)
        return res
