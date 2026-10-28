from typing import *


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        maxv = max(nums)
        if maxv < 2:
            return False
        # smallest prime factor sieve
        spf = list(range(maxv + 1))
        i = 2
        while i * i <= maxv:
            if spf[i] == i:
                for j in range(i * i, maxv + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        # DSU: indices 0..n-1, prime p is node n + p
        parent = list(range(n + maxv + 1))

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        for idx, v in enumerate(nums):
            if v == 1:
                return False
            x = v
            while x > 1:
                p = spf[x]
                while x % p == 0:
                    x //= p
                a = find(idx)
                b = find(n + p)
                if a != b:
                    parent[a] = b

        root = find(0)
        for idx in range(1, n):
            if find(idx) != root:
                return False
        return True
