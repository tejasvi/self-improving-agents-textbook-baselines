from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True
        max_val = max(nums)
        # Build smallest prime factor (SPF) sieve up to max_val
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val ** 0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        # DSU implementation
        parent = list(range(n))
        rank = [0] * n
        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(x: int, y: int):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
        # Map prime -> first index that contains it
        prime_to_index = {}
        for idx, val in enumerate(nums):
            x = val
            prev = 0
            while x > 1:
                p = spf[x]
                if p != prev:
                    if p in prime_to_index:
                        union(idx, prime_to_index[p])
                    else:
                        prime_to_index[p] = idx
                    prev = p
                while x % p == 0:
                    x //= p
        # Check connectivity
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        return True
