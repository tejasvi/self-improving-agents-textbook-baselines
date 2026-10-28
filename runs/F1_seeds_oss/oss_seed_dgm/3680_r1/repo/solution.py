from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # number of components

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        self.count -= 1

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Separate numbers greater than threshold (they are isolated)
        greater = [x for x in nums if x > threshold]
        isolated_count = len(greater)

        # Filter numbers <= threshold
        small = [x for x in nums if x <= threshold]
        if not small:
            return isolated_count

        # Map value to its index in the small list
        index_map = {val: i for i, val in enumerate(small)}
        uf = UnionFind(len(small))

        # For each multiple up to threshold, keep a representative index
        rep = [-1] * (threshold + 1)  # rep[m] = index of first number dividing m
        for i, val in enumerate(small):
            step = val
            for mult in range(step, threshold + 1, step):
                if rep[mult] == -1:
                    rep[mult] = i
                else:
                    uf.union(i, rep[mult])
        # total components = components among small + isolated greater numbers
        return uf.count + isolated_count
