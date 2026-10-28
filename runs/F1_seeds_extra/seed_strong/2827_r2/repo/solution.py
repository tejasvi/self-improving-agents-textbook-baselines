from typing import *


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False
        M = max(nums)
        # smallest prime factor sieve
        spf = list(range(M + 1))
        i = 2
        while i * i <= M:
            if spf[i] == i:
                for j in range(i * i, M + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1
        parent = list(range(M + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for v in nums:
            x = v
            first = spf[x]
            while x > 1:
                p = spf[x]
                ra, rb = find(first), find(p)
                if ra != rb:
                    parent[ra] = rb
                while x % p == 0:
                    x //= p
        root = find(spf[nums[0]])
        for v in nums:
            if find(spf[v]) != root:
                return False
        return True
