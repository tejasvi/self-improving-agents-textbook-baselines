from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums = sorted(nums)
        ans = 0
        r = 0  # sum over j < i of nums[j] * 2^(i-1-j)
        for x in nums:
            ans = (ans + x * x % MOD * ((x + r) % MOD)) % MOD
            r = (2 * r + x) % MOD
        return ans
