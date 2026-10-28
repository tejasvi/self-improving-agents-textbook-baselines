from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True
        # If any number is 1, it cannot connect to others unless all numbers are 1
        if any(x == 1 for x in nums):
            # If all are 1 and n==1 already handled, else false
            return False

        max_val = max(nums)
        # Sieve for smallest prime factor
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val ** 0.5) + 1):
            if spf[i] == i:  # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
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

        prime_to_index = {}
        for idx, val in enumerate(nums):
            # factorize using spf, collect distinct primes
            x = val
            prev_p = 0
            while x > 1:
                p = spf[x]
                if p != prev_p:
                    # union with previous index that had this prime
                    if p in prime_to_index:
                        union(idx, prime_to_index[p])
                    else:
                        prime_to_index[p] = idx
                    prev_p = p
                x //= p
                while x % p == 0:
                    x //= p
            # Note: above loop may skip some repeats, but we already advanced
        # After processing all, check if all have same root
        root0 = find(0)
        for i in range(1, n):
            if find(i) != root0:
                return False
        return True
