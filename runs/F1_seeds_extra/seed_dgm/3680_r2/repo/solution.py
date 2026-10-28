from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Nodes 0..threshold are used as union-find elements. Values in nums
        # that are <= threshold are "real" nodes; any m <= threshold is a
        # virtual node. Two real nodes a, b have lcm(a, b) <= threshold iff
        # they share a multiple m <= threshold, so joining each real value to
        # its multiples (<= threshold) reproduces exactly the graph's
        # connectivity. Virtual nodes only ever join real values that share
        # that multiple, so they never create spurious connections.
        parent = list(range(threshold + 1))

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        isolated = 0
        real = []
        for v in nums:
            if v > threshold:
                isolated += 1
            else:
                real.append(v)
                for m in range(2 * v, threshold + 1, v):
                    rv, rm = find(v), find(m)
                    if rv != rm:
                        parent[rm] = rv

        roots = {find(v) for v in real}
        return isolated + len(roots)
