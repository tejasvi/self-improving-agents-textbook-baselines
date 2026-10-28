from typing import List
from collections import defaultdict


def _square_free_part(x: int) -> int:
    """Return the square-free part of x (product of primes with odd exponent)."""
    result = 1
    p = 2
    while p * p <= x:
        if x % p == 0:
            count = 0
            while x % p == 0:
                x //= p
                count += 1
            if count % 2 == 1:
                result *= p
        p += 1
    return result * x


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # i * j is a perfect square iff i and j share the same square-free part.
        groups = defaultdict(int)
        for idx, val in enumerate(nums, start=1):
            groups[_square_free_part(idx)] += val
        return max(groups.values())
