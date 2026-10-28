from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        total = 0
        cur = 0  # sum_{j<i} a[j] * 2^(i-1-j)
        for x in a:
            # groups whose maximum is x (index i): min is x alone, or some earlier a[j]
            total = (total + x * x % MOD * ((x + cur) % MOD)) % MOD
            cur = (2 * cur + x) % MOD
        return total
