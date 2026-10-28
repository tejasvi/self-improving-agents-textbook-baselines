from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
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

        # buckets[m] = indices of nums that divide m (m <= threshold).
        # Two nodes are adjacent iff lcm(a, b) <= threshold, i.e. there is
        # some m <= threshold divisible by both; so union within each bucket.
        buckets = [[] for _ in range(threshold + 1)]
        for i, x in enumerate(nums):
            if x <= threshold:
                for m in range(x, threshold + 1, x):
                    buckets[m].append(i)

        for bucket in buckets:
            if len(bucket) > 1:
                first = bucket[0]
                for j in bucket[1:]:
                    union(first, j)

        return sum(1 for i in range(n) if find(i) == i)
