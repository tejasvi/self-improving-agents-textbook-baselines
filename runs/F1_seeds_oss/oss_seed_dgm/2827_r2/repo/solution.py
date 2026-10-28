from typing import List

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        # Path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return
        # Union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        self.components -= 1

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True

        max_val = max(nums)
        # Sieve for smallest prime factor (spf)
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val ** 0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        dsu = DSU(n)
        prime_to_index = {}
        for idx, value in enumerate(nums):
            x = value
            primes = set()
            while x > 1:
                p = spf[x]
                primes.add(p)
                while x % p == 0:
                    x //= p
            for p in primes:
                if p in prime_to_index:
                    dsu.union(idx, prime_to_index[p])
                else:
                    prime_to_index[p] = idx
        # After processing all numbers, check if all indices are connected
        return dsu.components == 1
