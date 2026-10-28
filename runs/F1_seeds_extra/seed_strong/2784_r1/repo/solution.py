from typing import *


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        total = 0
        acc = 0  # sum over j < i of a[j] * 2^(i-1-j)
        for x in a:
            total = (total + x * x % MOD * ((x + acc) % MOD)) % MOD
            acc = (2 * acc + x) % MOD
        return total
