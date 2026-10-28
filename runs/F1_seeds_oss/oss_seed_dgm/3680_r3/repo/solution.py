from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """Return number of connected components where an edge exists between i and j
        if lcm(nums[i], nums[j]) <= threshold.
        Numbers greater than threshold can never be connected to any other node because
        lcm(a, b) >= max(a, b). Hence each such number forms its own component.
        For numbers <= threshold we union all numbers that share a common multiple M (<=threshold).
        If two numbers a and b both divide the same M, then lcm(a, b) <= M <= threshold, so they
        are directly connected. By iterating over each possible M we can union the indices of the
        numbers that divide it.
        Complexity: O(threshold log threshold) time and O(threshold + n) memory.
        """
        # Separate numbers that are <= threshold (potentially connectable) from the rest.
        small = [x for x in nums if x <= threshold]
        large_cnt = len(nums) - len(small)  # each large number is an isolated component
        n = len(small)
        if n == 0:
            return large_cnt

        # Mapping from value to its index in `small` for DSU operations.
        index_of = {v: i for i, v in enumerate(small)}

        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] += 1

        # For each possible multiple M (1 .. threshold) collect indices of numbers that divide M.
        # Using a bucket list where bucket[m] holds indices of numbers dividing m.
        buckets: List[List[int]] = [[] for _ in range(threshold + 1)]
        for idx, val in enumerate(small):
            # iterate over multiples of val up to threshold
            for mult in range(val, threshold + 1, val):
                buckets[mult].append(idx)

        # Union all indices appearing in the same bucket (i.e., sharing a common multiple).
        for ids in buckets:
            if len(ids) > 1:
                first = ids[0]
                for other in ids[1:]:
                    union(first, other)

        # Count distinct roots among the small numbers.
        roots = {find(i) for i in range(n)}
        return large_cnt + len(roots)
