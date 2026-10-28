from typing import *
from collections import defaultdict


def _squarefree_part(k: int) -> int:
    res = 1
    d = 2
    while d * d <= k:
        while k % (d * d) == 0:
            k //= d * d
        if k % d == 0:
            res *= d
            k //= d
        d += 1
    return res * k


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        groups = defaultdict(int)
        for i, v in enumerate(nums, start=1):
            groups[_squarefree_part(i)] += v
        return max(groups.values()) if groups else 0
