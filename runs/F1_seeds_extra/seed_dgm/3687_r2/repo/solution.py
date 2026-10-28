from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # Per-depth state along the current root-to-node path.
        pathdist = [0] * (n + 1)   # distance from root to node at depth d
        leftbound = [0] * (n + 1)  # leftmost valid depth index for node at depth d
        last = {}                  # value -> depth of its most recent occurrence on path

        best_len = 0
        best_nodes = 1

        # Iterative DFS. Stack entries: (node, parent, depth, dist, enter flag, saved_prev)
        # On exit we restore last[val] to saved_prev.
        stack = [(0, -1, 0, 0, True)]
        saved = [None] * n  # saved previous last-occurrence depth per node
        while stack:
            node, parent, depth, dist, entering = stack.pop()
            if entering:
                val = nums[node]
                prev = last.get(val, -1)
                saved[node] = prev
                parent_left = leftbound[depth - 1] if depth > 0 else 0
                left = max(parent_left, prev + 1)
                leftbound[depth] = left
                pathdist[depth] = dist
                last[val] = depth

                length = dist - pathdist[left]
                nodes = depth - left + 1
                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len = length
                    best_nodes = nodes

                stack.append((node, parent, depth, dist, False))
                for child, w in adj[node]:
                    if child != parent:
                        stack.append((child, node, depth + 1, dist + w, True))
            else:
                val = nums[node]
                if saved[node] == -1:
                    del last[val]
                else:
                    last[val] = saved[node]

        return [best_len, best_nodes]
