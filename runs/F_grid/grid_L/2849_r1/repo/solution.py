from typing import List
from bisect import bisect_left, insort


class Solution:
    def sumImbalanceNumbers(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for l in range(n):
            vals = []  # sorted distinct values in nums[l..r]
            seen = set()
            cnt = 0  # number of adjacent distinct pairs with gap > 1
            for r in range(l, n):
                v = nums[r]
                if v not in seen:
                    seen.add(v)
                    idx = bisect_left(vals, v)
                    has_p = idx > 0
                    has_s = idx < len(vals)
                    if has_p and has_s:
                        if vals[idx] - vals[idx - 1] > 1:
                            cnt -= 1
                    if has_p and v - vals[idx - 1] > 1:
                        cnt += 1
                    if has_s and vals[idx] - v > 1:
                        cnt += 1
                    vals.insert(idx, v)
                total += cnt
        return total
