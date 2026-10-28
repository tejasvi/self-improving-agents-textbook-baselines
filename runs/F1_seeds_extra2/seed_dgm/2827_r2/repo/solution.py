from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if any(x == 1 for x in nums):
            return False

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

        components = n
        first_idx = {}  # prime -> first index having it
        for idx, x in enumerate(nums):
            while x > 1:
                p = spf[x]
                while x % p == 0:
                    x //= p
                if p in first_idx:
                    a, b = find(idx), find(first_idx[p])
                    if a != b:
                        parent[a] = b
                        components -= 1
                else:
                    first_idx[p] = idx
        return components == 1
