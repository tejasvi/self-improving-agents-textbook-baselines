from typing import List
from collections import defaultdict


class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        # f[v] = longest valid chain whose largest value is v
        f = defaultdict(int)
        for n in sorted(nums):
            # each element can end at n or n+1; compute both from old values
            new_n = f[n - 1] + 1
            new_n1 = f[n] + 1
            f[n] = max(f[n], new_n)
            f[n + 1] = max(f[n + 1], new_n1)
        return max(f.values()) if f else 0
