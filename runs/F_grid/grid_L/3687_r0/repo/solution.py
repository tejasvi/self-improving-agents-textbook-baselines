from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n          # distance from root
        pos = {}                # value -> depth index in current path (latest)
        P = [0] * (n + 1)       # P[d] = node at depth d on current path
        depth = [0] * n
        saved = [None] * n      # per node: (old L, value, old pos or None)
        best_len, best_cnt = 0, 1
        L = 0

        parent = [-1] * n
        stack = [(0, False)]
        while stack:
            v, exiting = stack.pop()
            if exiting:
                oldL, val, oldpos = saved[v]
                if oldpos is None:
                    del pos[val]
                else:
                    pos[val] = oldpos
                L = oldL
                continue

            d = depth[v]
            P[d] = v
            val = nums[v]
            oldpos = pos.get(val)
            saved[v] = (L, val, oldpos)
            if oldpos is not None and oldpos >= L:
                L = oldpos + 1
            pos[val] = d

            length = dist[v] - dist[P[L]]
            cnt = d - L + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len, best_cnt = length, cnt

            stack.append((v, True))
            for u, w in adj[v]:
                if u != parent[v]:
                    parent[u] = v
                    depth[u] = d + 1
                    dist[u] = dist[v] + w
                    stack.append((u, False))

        return [best_len, best_cnt]
