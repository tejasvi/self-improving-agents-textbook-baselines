from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        dist = [0] * n          # distance from root
        depth = [0] * n
        lo = [0] * n            # leftmost valid depth index for paths ending at node
        pd = [0] * (n + 1)      # pd[d] = dist of node at depth d on current path
        last = {}               # value -> depth of most recent ancestor on path
        saved = [0] * n         # previous last[val] for restoring on exit
        parent = [-1] * n

        best = 0
        cnt = 1
        # stack entries: (node, enter flag)
        stack = [(0, True)]
        while stack:
            v, enter = stack.pop()
            val = nums[v]
            if enter:
                d = depth[v]
                pd[d] = dist[v]
                prev = last.get(val, -1)
                saved[v] = prev
                last[val] = d
                lv = prev + 1
                p = parent[v]
                if p >= 0 and lo[p] > lv:
                    lv = lo[p]
                lo[v] = lv
                length = dist[v] - pd[lv]
                nodes = d - lv + 1
                if length > best:
                    best = length
                    cnt = nodes
                elif length == best and nodes < cnt:
                    cnt = nodes
                stack.append((v, False))
                for u, w in adj[v]:
                    if u != p:
                        parent[u] = v
                        depth[u] = d + 1
                        dist[u] = dist[v] + w
                        stack.append((u, True))
            else:
                if saved[v] < 0:
                    del last[val]
                else:
                    last[val] = saved[v]

        return [best, cnt]
