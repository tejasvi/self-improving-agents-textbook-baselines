from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len = 0
        best_nodes = 1
        last = {}                 # value -> depth of its latest occurrence on current path
        path_dist = [0] * (n + 1)  # path_dist[d] = distance from root to ancestor at depth d
        dist = [0] * n
        depth = [0] * n
        left_of = [0] * n         # smallest allowed ancestor depth for node
        saved_prev = [-1] * n     # previous last[val] before entering node
        parent = [-1] * n

        # iterative DFS: stack entries (node, is_exit)
        stack = [(0, False)]
        visited = [False] * n
        visited[0] = True
        # enter root
        while stack:
            v, exiting = stack.pop()
            if exiting:
                val = nums[v]
                if saved_prev[v] == -1:
                    del last[val]
                else:
                    last[val] = saved_prev[v]
                continue

            # entering v
            p = parent[v]
            d = 0 if p == -1 else depth[p] + 1
            depth[v] = d
            path_dist[d] = dist[v]
            val = nums[v]
            prev = last.get(val, -1)
            saved_prev[v] = prev
            last[val] = d
            base_left = 0 if p == -1 else left_of[p]
            left = max(base_left, prev + 1)
            left_of[v] = left

            cand_len = path_dist[d] - path_dist[left]
            cand_nodes = d - left + 1
            if cand_len > best_len or (cand_len == best_len and cand_nodes < best_nodes):
                best_len = cand_len
                best_nodes = cand_nodes

            stack.append((v, True))
            for u, w in adj[v]:
                if not visited[u]:
                    visited[u] = True
                    parent[u] = v
                    # distance to child: dist[v] + w, stored before child is entered
                    dist[u] = dist[v] + w
                    stack.append((u, False))

        return [best_len, best_nodes]
