from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums = sorted(nums)
        ans = 0
        s = 0  # S_i = sum_{j<i} nums[j] * 2^(i-j-1)
        for m in nums:
            ans = (ans + m * m % MOD * ((s + m) % MOD)) % MOD
            s = (2 * s + m) % MOD
        return ans
