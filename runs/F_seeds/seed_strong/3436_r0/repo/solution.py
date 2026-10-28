from typing import *


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        ans = abs(nums[0] - k)
        ors = set()  # distinct OR values of subarrays ending at current index
        for x in nums:
            new = {x}
            for v in ors:
                new.add(v | x)
            ors = new
            for v in ors:
                d = v - k if v >= k else k - v
                if d < ans:
                    ans = d
        return ans
