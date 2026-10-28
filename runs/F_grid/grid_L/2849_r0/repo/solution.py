from typing import List
from bisect import bisect_left, insort


class Solution:
    def sumImbalanceNumbers(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for i in range(n):
            vals = []          # sorted distinct values in nums[i..j]
            present = set()
            gaps = 0           # adjacent distinct pairs with difference > 1
            for j in range(i, n):
                v = nums[j]
                if v not in present:
                    present.add(v)
                    idx = bisect_left(vals, v)
                    p = vals[idx - 1] if idx > 0 else None
                    s = vals[idx] if idx < len(vals) else None
                    if p is not None and s is not None and s - p > 1:
                        gaps -= 1
                    if p is not None and v - p > 1:
                        gaps += 1
                    if s is not None and s - v > 1:
                        gaps += 1
                    vals.insert(idx, v)
                total += gaps
        return total
