from typing import List


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
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

        # DSU over indices [0, n) and prime nodes keyed by prime value offset by n.
        parent = list(range(n + max_val + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for idx, v in enumerate(nums):
            x = v
            while x > 1:
                p = spf[x]
                union(idx, n + p)
                while x % p == 0:
                    x //= p

        root = find(0)
        return all(find(i) == root for i in range(1, n))
