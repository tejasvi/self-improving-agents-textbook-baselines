from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False

        mx = max(nums)
        spf = list(range(mx + 1))
        i = 2
        while i * i <= mx:
            if spf[i] == i:
                for j in range(i * i, mx + 1, i):
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
        first = {}
        for idx, v in enumerate(nums):
            while v > 1:
                p = spf[v]
                while v % p == 0:
                    v //= p
                if p in first:
                    a, b = find(idx), find(first[p])
                    if a != b:
                        parent[a] = b
                        components -= 1
                else:
                    first[p] = idx
        return components == 1
