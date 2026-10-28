from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n          # distance from root
        depth = [0] * n
        pref = [0] * (n + 1)    # pref[d] = distance from root to the path node at depth d
        last = {}               # value -> depth of its latest occurrence on current path
        saved_prev = [-1] * n   # previous last[value] before entering node
        saved_left = [0] * n    # previous left boundary before entering node
        parent = [-1] * n

        best_len, best_nodes = 0, 1
        left = 0                # current leftmost depth of valid window
        # stack entries: (node, is_exit)
        stack = [(0, False)]
        while stack:
            v, is_exit = stack.pop()
            if is_exit:
                x = nums[v]
                if saved_prev[v] == -1:
                    del last[x]
                else:
                    last[x] = saved_prev[v]
                left = saved_left[v]
                continue

            d = depth[v]
            x = nums[v]
            prev = last.get(x, -1)
            saved_prev[v] = prev
            saved_left[v] = left
            left = max(left, prev + 1)
            last[x] = d
            pref[d] = dist[v]

            length = dist[v] - pref[left]
            nodes = d - left + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len, best_nodes = length, nodes

            stack.append((v, True))
            for c, w in adj[v]:
                if c != parent[v]:
                    parent[c] = v
                    depth[c] = d + 1
                    dist[c] = dist[v] + w
                    stack.append((c, False))

        return [best_len, best_nodes]
