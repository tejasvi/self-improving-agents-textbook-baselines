from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False

        maxv = max(nums)
        spf = list(range(maxv + 1))
        i = 2
        while i * i <= maxv:
            if spf[i] == i:
                for j in range(i * i, maxv + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        # Nodes 0..n-1 are indices; value-prime p is node n + p.
        parent = list(range(n + maxv + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for idx, v in enumerate(nums):
            while v > 1:
                p = spf[v]
                union(idx, n + p)
                while v % p == 0:
                    v //= p

        root = find(0)
        return all(find(i) == root for i in range(1, n))
