from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        total = 0
        r = 0  # R_i = sum_{j<i} a[j] * 2^(i-j-1)
        for x in a:
            total = (total + x * x % MOD * ((x + r) % MOD)) % MOD
            r = (2 * r + x) % MOD
        return total
