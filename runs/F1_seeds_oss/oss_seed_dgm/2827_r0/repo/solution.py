from typing import List

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True
        # If any number is 1, it cannot connect to others (since gcd(1, x) = 1)
        if any(x == 1 for x in nums):
            return False
        max_val = max(nums)
        # Compute smallest prime factor for every number up to max_val
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val ** 0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        dsu = DSU(n)
        prime_to_index = {}
        for idx, val in enumerate(nums):
            x = val
            last_p = 0
            while x > 1:
                p = spf[x]
                if p != last_p:
                    if p in prime_to_index:
                        dsu.union(idx, prime_to_index[p])
                    else:
                        prime_to_index[p] = idx
                    last_p = p
                # divide out all occurrences of p
                while x % p == 0:
                    x //= p
        # Verify all indices belong to the same connected component
        root = dsu.find(0)
        for i in range(1, n):
            if dsu.find(i) != root:
                return False
        return True
