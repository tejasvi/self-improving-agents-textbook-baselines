from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n          # distance from root
        path_dist = [0] * (n + 1)  # distance of ancestor at each depth on current path
        last = {}               # value -> depth of its nearest occurrence on current path
        best_len = -1
        best_cnt = 1
        left = 0                # minimal depth allowed as start of special path

        # stack entries: (node, parent, depth, prev_last, prev_left) for exit, or enter marker
        stack = [(0, -1, 0, None, None)]
        while stack:
            item = stack.pop()
            v, p, d, prev_last, prev_left = item
            if prev_last is not None:
                # exit marker: restore state
                val = nums[v]
                if prev_last == -1:
                    del last[val]
                else:
                    last[val] = prev_last
                left = prev_left
                continue

            val = nums[v]
            pl = last.get(val, -1)
            # push exit marker
            stack.append((v, p, d, pl, left))
            left = max(left, pl + 1)
            last[val] = d
            path_dist[d] = dist[v]

            length = dist[v] - path_dist[left]
            cnt = d - left + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len = length
                best_cnt = cnt

            for u, w in adj[v]:
                if u != p:
                    dist[u] = dist[v] + w
                    stack.append((u, v, d + 1, None, None))

        return [best_len, best_cnt]
