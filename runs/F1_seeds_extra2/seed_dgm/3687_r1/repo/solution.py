from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        last = {}                      # value -> depth of nearest ancestor with that value
        path_dist = [0] * (n + 1)      # path_dist[d] = distance from root to ancestor at depth d
        best_len, best_nodes = 0, 1
        parent = [-1] * n
        depth = [0] * n
        dist = [0] * n
        # saved previous occurrence depth for restoring on exit
        saved = [-1] * n
        # L[v]: minimal allowed ancestor depth for paths ending at v
        L = [0] * n

        stack = [(0, False)]
        while stack:
            v, exiting = stack.pop()
            if exiting:
                val = nums[v]
                last[val] = saved[v]
                continue
            p = parent[v]
            if p == -1:
                depth[v] = 0
                dist[v] = 0
                base_L = 0
            else:
                depth[v] = depth[p] + 1
                base_L = L[p]
            d = depth[v]
            path_dist[d] = dist[v]
            val = nums[v]
            prev = last.get(val, -1)
            saved[v] = prev
            cur_L = max(base_L, prev + 1)
            L[v] = cur_L
            last[val] = d

            length = dist[v] - path_dist[cur_L]
            nodes = d - cur_L + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len, best_nodes = length, nodes

            stack.append((v, True))
            for u, w in adj[v]:
                if u != p:
                    parent[u] = v
                    dist[u] = dist[v] + w
                    stack.append((u, False))
        return [best_len, best_nodes]
