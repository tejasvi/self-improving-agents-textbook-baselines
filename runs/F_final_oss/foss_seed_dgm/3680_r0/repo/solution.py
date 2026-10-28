from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # number of disjoint sets

    def find(self, x: int) -> int:
        # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return
        # union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        self.count -= 1

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        # Map each number to its index for union‑find
        idx_of = {val: i for i, val in enumerate(nums)}
        # Separate numbers that can possibly have edges (<= threshold)
        small_nums = [val for val in nums if val <= threshold]
        if not small_nums:
            # All numbers are > threshold, each is isolated
            return n

        # Union‑find over all indices (including large numbers, they will stay isolated)
        uf = UnionFind(n)
        # First seen index for each multiple up to threshold
        first_idx = [-1] * (threshold + 1)
        for val in small_nums:
            i = idx_of[val]
            step = val
            # iterate over multiples of val up to threshold
            for m in range(step, threshold + 1, step):
                if first_idx[m] == -1:
                    first_idx[m] = i
                else:
                    uf.union(i, first_idx[m])
        # Count distinct components
        root_set = set()
        isolated_large = 0
        for i, val in enumerate(nums):
            if val > threshold:
                isolated_large += 1
            else:
                root_set.add(uf.find(i))
        return isolated_large + len(root_set)
