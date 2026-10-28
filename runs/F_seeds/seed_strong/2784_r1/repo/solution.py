from typing import *

MOD = 10**9 + 7


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        a = sorted(nums)
        f = 0  # f = sum_{j<i} a[j] * 2^(i-j-1)
        ans = 0
        for x in a:
            ans = (ans + x * x % MOD * ((f + x) % MOD)) % MOD
            f = (2 * f + x) % MOD
        return ans
