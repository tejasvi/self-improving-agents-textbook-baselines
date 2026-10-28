from typing import List


class Solution:
    def maxSum(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        cnt = [0] * 31
        for x in nums:
            b = 0
            while x:
                if x & 1:
                    cnt[b] += 1
                x >>= 1
                b += 1
        total = 0
        for _ in range(k):
            val = 0
            for b in range(31):
                if cnt[b] > 0:
                    val |= 1 << b
                    cnt[b] -= 1
            total = (total + val * val) % MOD
        return total
