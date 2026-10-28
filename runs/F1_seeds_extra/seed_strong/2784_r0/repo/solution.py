from typing import *


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        total = 0
        f = 0  # sum_{j<i} a_j * 2^(i-j-1) mod MOD
        for x in a:
            total = (total + x * x % MOD * ((x + f) % MOD)) % MOD
            f = (2 * f + x) % MOD
        return total
