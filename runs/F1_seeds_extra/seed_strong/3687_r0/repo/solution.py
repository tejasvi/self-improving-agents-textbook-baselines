from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n              # distance from root
        path_dist = [0] * (n + 1)   # path_dist[depth] = dist of ancestor at depth on current path
        last = {}                   # value -> depth of deepest ancestor (on current path) with that value
        best_len = 0
        best_nodes = 1

        # stack entries: (node, parent, depth, left_depth_of_parent) for enter
        #                (None, value, prev_last, ...) for exit
        stack = [(0, -1, 0, 0)]
        # Record for exit: value and previous last depth
        prev_of = [None] * n
        while stack:
            item = stack.pop()
            if item[0] is None:
                _, v, prev = item
                if prev is None:
                    del last[v]
                else:
                    last[v] = prev
                continue
            u, p, d, lp = item
            v = nums[u]
            prev = last.get(v)
            left = lp
            if prev is not None and prev + 1 > left:
                left = prev + 1
            last[v] = d
            path_dist[d] = dist[u]
            length = dist[u] - path_dist[left]
            nodes = d - left + 1
            if length > best_len:
                best_len = length
                best_nodes = nodes
            elif length == best_len and nodes < best_nodes:
                best_nodes = nodes
            # schedule exit (restore last[v]) before children
            stack.append((None, v, prev))
            for w, wt in adj[u]:
                if w != p:
                    dist[w] = dist[u] + wt
                    stack.append((w, u, d + 1, left))
        return [best_len, best_nodes]
