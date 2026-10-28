from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False

        # smallest prime factor sieve up to max value
        m = max(nums)
        spf = list(range(m + 1))
        i = 2
        while i * i <= m:
            if spf[i] == i:
                for j in range(i * i, m + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        first_seen = {}
        for idx, v in enumerate(nums):
            x = v
            while x > 1:
                p = spf[x]
                while x % p == 0:
                    x //= p
                if p in first_seen:
                    union(idx, first_seen[p])
                else:
                    first_seen[p] = idx

        root = find(0)
        return all(find(k) == root for k in range(n))
