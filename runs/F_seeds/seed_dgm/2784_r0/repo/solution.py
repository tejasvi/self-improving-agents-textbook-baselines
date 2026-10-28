from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums = sorted(nums)
        ans = 0
        acc = 0  # sum over j < i of nums[j] * 2^(i-1-j)
        for x in nums:
            # x is the maximum; min is x itself or any smaller element
            ans = (ans + x * x % MOD * ((acc + x) % MOD)) % MOD
            acc = (acc * 2 + x) % MOD
        return ans
