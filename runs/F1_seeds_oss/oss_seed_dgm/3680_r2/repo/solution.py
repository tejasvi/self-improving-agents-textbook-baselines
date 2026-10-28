from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Numbers greater than threshold cannot be connected to any other node because
        # lcm(a, b) >= max(a, b) > threshold. Each such number forms its own component.
        big_count = sum(1 for x in nums if x > threshold)

        # Consider only numbers <= threshold.
        small = [x for x in nums if x <= threshold]
        if not small:
            # Only the big numbers exist.
            return big_count

        # Map each small number to an index for union‑find.
        index = {x: i for i, x in enumerate(small)}
        parent = list(range(len(small)))
        rank = [0] * len(small)

        def find(u: int) -> int:
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u: int, v: int) -> None:
            ru, rv = find(u), find(v)
            if ru == rv:
                return
            if rank[ru] < rank[rv]:
                parent[ru] = rv
            elif rank[ru] > rank[rv]:
                parent[rv] = ru
            else:
                parent[rv] = ru
                rank[ru] += 1

        # For each possible multiple up to threshold, keep the first number that divides it.
        # When another number also divides the same multiple, union them.
        first = [-1] * (threshold + 1)
        for num in small:
            # iterate over multiples of num up to threshold
            step = num
            for m in range(step, threshold + 1, step):
                if first[m] == -1:
                    first[m] = num
                else:
                    union(index[num], index[first[m]])

        # Count distinct sets among small numbers.
        root_set = set()
        for i in range(len(small)):
            root_set.add(find(i))
        return big_count + len(root_set)
