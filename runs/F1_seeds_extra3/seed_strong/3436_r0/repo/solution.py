from typing import *


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        ans = float('inf')
        ors = set()  # distinct ORs of subarrays ending at the current index
        for x in nums:
            new = {o | x for o in ors}
            new.add(x)
            for v in new:
                d = k - v if k >= v else v - k
                if d < ans:
                    ans = d
            ors = new
        return ans
