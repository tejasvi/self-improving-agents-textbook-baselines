from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums = sorted(nums)
        res = 0
        # r = sum over i < j of nums[i] * 2^(j-i-1)
        r = 0
        for x in nums:
            # x as maximum: subgroups with min = nums[i] (i<j) or min = x itself
            res = (res + x * x % MOD * ((x + r) % MOD)) % MOD
            r = (2 * r + x) % MOD
        return res
