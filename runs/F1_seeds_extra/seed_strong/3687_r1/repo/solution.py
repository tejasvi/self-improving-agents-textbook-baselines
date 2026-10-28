from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        D = [0] * n          # distance from root
        depth = [0] * n
        left = [0] * n       # smallest depth allowed for path ending at node
        path = [0] * n       # path[d] = node at depth d on current root path
        last = {}            # value -> depth of most recent ancestor (on current path) with that value
        best_len = 0
        best_cnt = 1

        # iterative DFS; stack entries: (node, parent, saved_prev_last or None, is_exit)
        # when entering a node we record the previous last-depth for its value to restore on exit
        stack = [(0, -1, 0, False)]
        saved = [None] * n
        while stack:
            node, par, _, is_exit = stack.pop()
            if is_exit:
                v = nums[node]
                if saved[node] is None:
                    del last[v]
                else:
                    last[v] = saved[node]
                continue
            if par == -1:
                d = 0
                D[node] = 0
                lp = 0
            else:
                d = depth[par] + 1
                lp = left[par]
            depth[node] = d
            path[d] = node
            v = nums[node]
            prev = last.get(v)
            saved[node] = prev
            # window must start strictly after the previous same-valued ancestor
            ls = lp
            if prev is not None and prev + 1 > ls:
                ls = prev + 1
            left[node] = ls
            last[v] = d
            # candidate: start at depth ls
            start = path[ls]
            length = D[node] - D[start]
            cnt = d - ls + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len = length
                best_cnt = cnt
            stack.append((node, par, 0, True))
            for c, w in adj[node]:
                if c != par:
                    D[c] = D[node] + w
                    stack.append((c, node, 0, False))
        return [best_len, best_cnt]
