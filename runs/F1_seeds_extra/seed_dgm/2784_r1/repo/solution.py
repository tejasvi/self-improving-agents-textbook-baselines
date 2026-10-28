from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        total = 0
        s = 0  # sum over j < i of a[j] * 2^(i-j-1)
        for x in a:
            total = (total + x * x % MOD * ((x + s) % MOD)) % MOD
            s = (2 * s + x) % MOD
        return total
