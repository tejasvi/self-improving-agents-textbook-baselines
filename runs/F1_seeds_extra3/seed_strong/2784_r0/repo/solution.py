from typing import *


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        total = 0
        R = 0  # sum_{j<i} a[j] * 2^(i-j-1)
        for x in a:
            total = (total + x * x % MOD * ((x + R) % MOD)) % MOD
            R = (2 * R + x) % MOD
        return total
