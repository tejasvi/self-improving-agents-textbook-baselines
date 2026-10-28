from typing import List

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

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


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Separate numbers into those that can possibly have edges (<= threshold)
        # and those that are guaranteed to be isolated (> threshold).
        small = []          # values <= threshold
        large_isolated = 0  # count of values > threshold
        for v in nums:
            if v <= threshold:
                small.append(v)
            else:
                large_isolated += 1

        k = len(small)
        if k == 0:
            # All numbers are isolated.
            return large_isolated

        dsu = DSU(k)
        # For fast access, we need the index of each small number.
        # We'll iterate over numbers and union them via common multiples.
        first = [-1] * (threshold + 1)  # first index of a number dividing the multiple

        for idx, val in enumerate(small):
            # Iterate over multiples of val up to threshold.
            step = val
            for m in range(step, threshold + 1, step):
                if first[m] == -1:
                    first[m] = idx
                else:
                    dsu.union(idx, first[m])

        # Count distinct roots among small numbers.
        roots = set()
        for i in range(k):
            roots.add(dsu.find(i))

        return large_isolated + len(roots)
