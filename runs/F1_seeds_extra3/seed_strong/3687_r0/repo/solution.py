from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        parent = [-1] * n
        seen = [False] * n
        seen[0] = True
        order = [0]
        for x in order:  # BFS to fix parents
            for y, _ in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    parent[y] = x
                    order.append(y)

        last = {}                  # value -> depth of its node on the current root path
        saved = [None] * n         # previous last[] entry of each node, restored on exit
        anc_dist = [0] * (n + 1)   # anc_dist[k] = root distance of the current path node at depth k
        best_len, best_cnt = 0, 1
        # enter: (node, depth, dist_from_root, left_depth); exit: (node, -1, 0, 0)
        stack = [(0, 0, 0, 0)]
        while stack:
            node, d, dist, left = stack.pop()
            val = nums[node]
            if d < 0:  # exit: restore map
                if saved[node] is None:
                    del last[val]
                else:
                    last[val] = saved[node]
                continue
            prev = last.get(val)
            saved[node] = prev
            if prev is not None and prev + 1 > left:
                left = prev + 1
            last[val] = d
            anc_dist[d] = dist
            length = dist - anc_dist[left]
            cnt = d - left + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len, best_cnt = length, cnt
            stack.append((node, -1, 0, 0))
            p = parent[node]
            for child, w in adj[node]:
                if child != p:
                    stack.append((child, d + 1, dist + w, left))
        return [best_len, best_cnt]
