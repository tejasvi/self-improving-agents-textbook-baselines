from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True
        # If any number is 1, it cannot connect to others.
        if any(x == 1 for x in nums):
            return False
        max_val = max(nums)
        # Build smallest prime factor (SPF) array up to max_val
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val ** 0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        uf = UnionFind(n)
        prime_to_index = {}
        for idx, val in enumerate(nums):
            # factorize val into distinct primes using spf
            x = val
            seen_primes = set()
            while x > 1:
                p = spf[x]
                seen_primes.add(p)
                while x % p == 0:
                    x //= p
            for p in seen_primes:
                if p in prime_to_index:
                    uf.union(idx, prime_to_index[p])
                else:
                    prime_to_index[p] = idx
        # All nodes must share the same root
        root = uf.find(0)
        for i in range(1, n):
            if uf.find(i) != root:
                return False
        return True
