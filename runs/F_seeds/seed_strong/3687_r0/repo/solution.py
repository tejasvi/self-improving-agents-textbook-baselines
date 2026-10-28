from typing import *


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        pref = [0] * n
        depth = [0] * n
        parent = [-1] * n
        path = [0] * (n + 1)          # path[d] = node at depth d on current root path
        last = {}                     # value -> depth of its latest occurrence on path
        best_len, best_nodes = 0, 1

        # stack entries: (node, exit_flag, saved_left, saved_prev_last)
        # enter: node >= 0 ; exit encoded as ~node
        left = 0                      # window start depth on current path
        saved_left = [0] * n
        saved_prev = [-1] * n
        stack = [0]
        while stack:
            t = stack.pop()
            if t < 0:
                v = ~t
                x = nums[v]
                if saved_prev[v] == -1:
                    del last[x]
                else:
                    last[x] = saved_prev[v]
                left = saved_left[v]
                continue
            v = t
            d = depth[v]
            path[d] = v
            x = nums[v]
            prev = last.get(x, -1)
            saved_prev[v] = prev
            saved_left[v] = left
            if prev + 1 > left:
                left = prev + 1
            last[x] = d
            # topmost valid ancestor is at depth `left`
            top = path[left]
            length = pref[v] - pref[top]
            nodes = d - left + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len, best_nodes = length, nodes
            stack.append(~v)
            for u, w in adj[v]:
                if u != parent[v]:
                    parent[u] = v
                    depth[u] = d + 1
                    pref[u] = pref[v] + w
                    stack.append(u)
        return [best_len, best_nodes]
