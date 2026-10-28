from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        last = {}                 # value -> depth of its nearest occurrence on current path
        pd = [0] * (n + 1)        # pd[d] = distance from root to the path node at depth d
        saved = [None] * n        # per node: (old_left, old_last_depth_of_value)
        best_len = 0
        best_nodes = 1
        left = 0                  # smallest depth such that path nodes [left..d] are unique
        # stack entries: (node, parent, depth, dist, exiting)
        stack = [(0, -1, 0, 0, False)]
        while stack:
            node, par, d, dist, exiting = stack.pop()
            if exiting:
                old_left, old_last = saved[node]
                left = old_left
                x = nums[node]
                if old_last == -1:
                    del last[x]
                else:
                    last[x] = old_last
                continue
            x = nums[node]
            prev = last.get(x, -1)
            saved[node] = (left, prev)
            if prev + 1 > left:
                left = prev + 1
            last[x] = d
            pd[d] = dist
            length = dist - pd[left]
            nodes = d - left + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes
            stack.append((node, par, d, dist, True))
            for nb, w in adj[node]:
                if nb != par:
                    stack.append((nb, node, d + 1, dist + w, False))
        return [best_len, best_nodes]
