from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        t = threshold
        parent = list(range(t + 1))

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        # Numbers above threshold have lcm > threshold with everything: isolated.
        isolated = 0
        valid = []
        for x in nums:
            if x > t:
                isolated += 1
            else:
                valid.append(x)

        # Union each valid value with all of its multiples <= threshold.
        for x in valid:
            for m in range(2 * x, t + 1, x):
                ra, rb = find(x), find(m)
                if ra != rb:
                    parent[ra] = rb

        roots = {find(x) for x in valid}
        return isolated + len(roots)
