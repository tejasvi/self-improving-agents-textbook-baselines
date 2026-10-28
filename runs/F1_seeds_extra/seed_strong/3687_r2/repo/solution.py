from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        occ = {}              # value -> stack of depths on current root path
        path = [0] * (n + 1)  # path[d] = node at depth d on current root path
        dist = [0] * n        # distance from root
        depth = [0] * n
        saved = [0] * n       # L before entering node
        parent = [-1] * n
        best_len = 0
        best_nodes = 1
        L = 0                 # shallowest allowed ancestor depth

        stack = [(0, 0)]
        while stack:
            u, flag = stack.pop()
            if flag == 1:
                occ[nums[u]].pop()
                L = saved[u]
                continue
            p = parent[u]
            D = 0 if p < 0 else depth[p] + 1
            depth[u] = D
            path[D] = u
            v = nums[u]
            lst = occ.get(v)
            if lst is None:
                lst = []
                occ[v] = lst
            saved[u] = L
            if lst and lst[-1] + 1 > L:
                L = lst[-1] + 1
            lst.append(D)
            length = dist[u] - dist[path[L]]
            nodes = D - L + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes
            stack.append((u, 1))
            for c, w in adj[u]:
                if c != p:
                    parent[c] = u
                    dist[c] = dist[u] + w
                    stack.append((c, 0))
        return [best_len, best_nodes]
