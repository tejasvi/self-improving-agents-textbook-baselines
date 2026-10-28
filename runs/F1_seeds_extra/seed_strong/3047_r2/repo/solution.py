from typing import *


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)
        # Square-free part of each 1-indexed position; indices with equal
        # square-free part form a complete set.
        # Use a sieve for the smallest prime factor up to n.
        spf = list(range(n + 1))
        i = 2
        while i * i <= n:
            if spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        groups = {}
        for idx in range(1, n + 1):
            x = idx
            sf = 1
            while x > 1:
                p = spf[x]
                c = 0
                while x % p == 0:
                    x //= p
                    c ^= 1
                if c:
                    sf *= p
            groups[sf] = groups.get(sf, 0) + nums[idx - 1]
        return max(groups.values()) if groups else 0
