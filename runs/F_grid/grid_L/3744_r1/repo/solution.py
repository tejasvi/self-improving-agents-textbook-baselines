from typing import List


def _digit_sum_prefix(n: int) -> int:
    """Sum of base-4 digit lengths of all integers in [1, n]."""
    total = 0
    k = 1
    lo = 1  # 4^(k-1)
    while lo <= n:
        hi = min(n, lo * 4 - 1)
        total += k * (hi - lo + 1)
        lo *= 4
        k += 1
    return total


def _digits4(x: int) -> int:
    d = 0
    while x:
        x //= 4
        d += 1
    return d


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        res = 0
        for l, r in queries:
            s = _digit_sum_prefix(r) - _digit_sum_prefix(l - 1)
            res += max(_digits4(l), (s + 1) // 2)
        return res
