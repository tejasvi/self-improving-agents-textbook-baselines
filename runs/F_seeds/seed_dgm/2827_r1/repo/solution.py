from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if any(x == 1 for x in nums):
            return False

        max_val = max(nums)
        spf = list(range(max_val + 1))
        i = 2
        while i * i <= max_val:
            if spf[i] == i:
                for j in range(i * i, max_val + 1, i):
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
        first_index = {}  # prime -> first index having it
        for idx, x in enumerate(nums):
            while x > 1:
                p = spf[x]
                while x % p == 0:
                    x //= p
                if p in first_index:
                    ra, rb = find(first_index[p]), find(idx)
                    if ra != rb:
                        parent[ra] = rb
                        components -= 1
                else:
                    first_index[p] = idx
        return components == 1
