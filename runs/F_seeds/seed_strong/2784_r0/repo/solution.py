from typing import *


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        ans = 0
        r = 0  # sum_{j<i} a[j] * 2^(i-1-j)
        for x in a:
            ans = (ans + x * x % MOD * ((x + r) % MOD)) % MOD
            r = (2 * r + x) % MOD
        return ans
