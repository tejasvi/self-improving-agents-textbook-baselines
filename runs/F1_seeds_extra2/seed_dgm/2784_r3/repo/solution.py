from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        arr = sorted(nums)
        ans = 0
        f = 0  # sum_{j<i} arr[j] * 2^(i-j-1)
        for x in arr:
            ans = (ans + x * x % MOD * ((x + f) % MOD)) % MOD
            f = (2 * f + x) % MOD
        return ans
