from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        ans = 0
        f = 0  # sum_{j<i} a[j] * 2^(i-1-j)
        for x in a:
            ans = (ans + x * x % MOD * ((x + f) % MOD)) % MOD
            f = (2 * f + x) % MOD
        return ans
