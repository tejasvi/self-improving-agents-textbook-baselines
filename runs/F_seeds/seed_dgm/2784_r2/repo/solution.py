from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        ans = 0
        s = 0  # sum_{j<i} a[j] * 2^(i-j-1)
        for x in a:
            # x as maximum: subsets whose min is x (singleton) or some a[j] (j<i)
            ans = (ans + x * x % MOD * ((x + s) % MOD)) % MOD
            s = (2 * s + x) % MOD
        return ans
