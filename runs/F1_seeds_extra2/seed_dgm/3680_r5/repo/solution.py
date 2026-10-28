from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        parent = list(range(T + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        # Two values a, b (<= T) are adjacent iff both divide some m <= T.
        # Connect each value x to all of its multiples <= T.
        valid = [x for x in nums if x <= T]
        for x in valid:
            for m in range(2 * x, T + 1, x):
                union(x, m)

        roots = set()
        isolated = 0
        for x in nums:
            if x > T:
                isolated += 1
            else:
                roots.add(find(x))
        return len(roots) + isolated
