from typing import *


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False
        M = max(nums)
        spf = list(range(M + 1))
        i = 2
        while i * i <= M:
            if spf[i] == i:
                for j in range(i * i, M + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1
        # nodes: 0..n-1 indices, n..n+M primes
        parent = list(range(n + M + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for idx, v in enumerate(nums):
            x = v
            while x > 1:
                p = spf[x]
                a, b = find(idx), find(n + p)
                if a != b:
                    parent[a] = b
                while x % p == 0:
                    x //= p
        root = find(0)
        return all(find(k) == root for k in range(n))
