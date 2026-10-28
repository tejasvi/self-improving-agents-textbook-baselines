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
        left = [0] * n          # leftmost valid depth index for paths ending at node
        saved = [-1] * n        # previous last-depth of nums[node] before entering node
        path = [0] * n          # path[d] = node at depth d on current root path
        last = {}               # value -> depth of its latest occurrence on current path
        parent = [-1] * n

        best_len = 0
        best_nodes = 1
        stack = [(0, False)]
        visited = [False] * n
        visited[0] = True
        while stack:
            v, exiting = stack.pop()
            if exiting:
                val = nums[v]
                if saved[v] == -1:
                    last.pop(val, None)
                else:
                    last[val] = saved[v]
                continue

            p = parent[v]
            d = depth[v]
            path[d] = v
            val = nums[v]
            prev = last.get(val, -1)
            saved[v] = prev
            last[val] = d
            pl = left[p] if p != -1 else 0
            lv = max(pl, prev + 1)
            left[v] = lv

            length = dist[v] - dist[path[lv]]
            nodes = d - lv + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes

            stack.append((v, True))
            for c, w in adj[v]:
                if not visited[c]:
                    visited[c] = True
                    parent[c] = v
                    depth[c] = d + 1
                    dist[c] = dist[v] + w
                    stack.append((c, False))

        return [best_len, best_nodes]
