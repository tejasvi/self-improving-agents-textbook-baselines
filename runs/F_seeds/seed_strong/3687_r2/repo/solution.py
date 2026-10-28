from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len = 0
        best_cnt = 1
        # last[x] = depth of deepest node on current path with value x, or -1
        last = {}
        # pref_by_depth[d] = root distance of the ancestor at depth d on current path
        pref_by_depth = []
        left = 0  # smallest depth at which a special path may start

        # Stack entries: (node, parent, depth, dist, state)
        # state 0 = enter, 1 = exit (restore saved values)
        saved = {}
        stack = [(0, -1, 0, 0, 0)]
        while stack:
            node, parent, depth, dist, state = stack.pop()
            if state == 1:
                x = nums[node]
                last[x] = saved[node][0]
                left = saved[node][1]
                pref_by_depth.pop()
                continue
            x = nums[node]
            prev = last.get(x, -1)
            saved[node] = (prev, left)
            if prev + 1 > left:
                left = prev + 1
            last[x] = depth
            # pref_by_depth has length depth before push
            pref_by_depth.append(dist)
            length = dist - pref_by_depth[left]
            cnt = depth - left + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len = length
                best_cnt = cnt
            stack.append((node, parent, depth, dist, 1))
            for nb, w in adj[node]:
                if nb != parent:
                    stack.append((nb, node, depth + 1, dist + w, 0))
        return [best_len, best_cnt]
