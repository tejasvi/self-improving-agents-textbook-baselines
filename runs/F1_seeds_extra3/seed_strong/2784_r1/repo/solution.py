from typing import *

MOD = 10**9 + 7


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        a = sorted(nums)
        ans = 0
        f = 0  # sum_{j<i} a[j] * 2^(i-j-1)
        for x in a:
            # x as maximum: min is x itself (x^3) or some a[j] with j<i
            ans = (ans + x * x % MOD * ((x + f) % MOD)) % MOD
            f = (2 * f + x) % MOD
        return ans
