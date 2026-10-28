from typing import List


class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        ans = 0
        s = 0  # sum over j < i of a_j * 2^(i-j-1)
        for x in a:
            # x is the maximum; minimum is a_j (j <= i) or x itself
            ans = (ans + x * x % MOD * ((x + s) % MOD)) % MOD
            s = (2 * s + x) % MOD
        return ans
