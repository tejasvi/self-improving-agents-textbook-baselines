from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n          # distance from root
        path = [0] * (n + 1)    # path[d] = ancestor node at depth d on current root path
        left = [0] * n          # leftmost valid ancestor depth for node
        last = {}               # value -> depth of its latest occurrence on current path
        best_len = 0
        best_nodes = 1

        # stack entries: (node, parent, depth, saved_prev_depth_for_value, phase)
        # phase 0 = enter, phase 1 = exit
        parent = [-1] * n
        depth = [0] * n
        saved = [None] * n
        stack = [(0, 0)]
        while stack:
            v, phase = stack.pop()
            if phase == 1:
                # exit: restore last occurrence of nums[v]
                prev = saved[v]
                if prev is None:
                    del last[nums[v]]
                else:
                    last[nums[v]] = prev
                continue

            p = parent[v]
            if p == -1:
                d = 0
                dist[v] = 0
                lp = 0
            else:
                d = depth[p] + 1
                lp = left[p]
            depth[v] = d
            path[d] = v

            val = nums[v]
            prev = last.get(val)
            saved[v] = prev
            start = lp
            if prev is not None and prev + 1 > start:
                start = prev + 1
            left[v] = start
            last[val] = d

            length = dist[v] - dist[path[start]]
            nodes = d - start + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes

            stack.append((v, 1))
            for u, w in adj[v]:
                if u != p:
                    parent[u] = v
                    dist[u] = dist[v] + w
                    stack.append((u, 0))

        return [best_len, best_nodes]
