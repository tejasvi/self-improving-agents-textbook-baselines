from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False

        maxv = max(nums)
        # smallest prime factor sieve
        spf = list(range(maxv + 1))
        i = 2
        while i * i <= maxv:
            if spf[i] == i:
                for j in range(i * i, maxv + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        # DSU: nodes 0..n-1 are indices, n + p is prime p
        parent = list(range(n + maxv + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for idx, v in enumerate(nums):
            x = v
            while x > 1:
                p = spf[x]
                ra, rb = find(idx), find(n + p)
                if ra != rb:
                    parent[ra] = rb
                while x % p == 0:
                    x //= p

        root = find(0)
        return all(find(i) == root for i in range(1, n))
