from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        # Values > threshold can never share an edge (lcm >= value > threshold).
        isolated = 0
        small = []
        for x in nums:
            if x > T:
                isolated += 1
            else:
                small.append(x)

        parent = {x: x for x in small}

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                return True
            return False

        # owner[L] = some value x (<= T) dividing L; all values dividing L are
        # pairwise connected via lcm <= L <= T.
        owner = [0] * (T + 1)
        for x in small:
            for m in range(x, T + 1, x):
                if owner[m] == 0:
                    owner[m] = x
                else:
                    union(x, owner[m])

        roots = {find(x) for x in small}
        return isolated + len(roots)
