from typing import List


class Solution:
    def timeTaken(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # w(k): cost of entering node k (1 if odd, 2 if even)
        w = [1 if k % 2 == 1 else 2 for k in range(n)]

        # BFS order from root 0
        parent = [-1] * n
        order = []
        visited = [False] * n
        visited[0] = True
        stack = [0]
        while stack:
            v = stack.pop()
            order.append(v)
            for u in adj[v]:
                if not visited[u]:
                    visited[u] = True
                    parent[u] = v
                    stack.append(u)

        # down[v]: max cost from v to a node in its subtree (excluding v's own cost)
        down = [0] * n
        for v in reversed(order):
            p = parent[v]
            if p != -1:
                cand = w[v] + down[v]
                if cand > down[p]:
                    down[p] = cand

        # up[v]: max cost from v to a node outside v's subtree (0 if none)
        up = [0] * n
        for v in order:
            # top two values among children contributions
            best1 = 0
            best2 = 0
            best1_child = -1
            for c in adj[v]:
                if c == parent[v]:
                    continue
                val = w[c] + down[c]
                if val > best1:
                    best2 = best1
                    best1 = val
                    best1_child = c
                elif val > best2:
                    best2 = val
            base = max(up[v], 0)
            for c in adj[v]:
                if c == parent[v]:
                    continue
                sib = best2 if c == best1_child else best1
                up[c] = w[v] + max(base, sib)

        res = [0] * n
        for v in range(n):
            res[v] = max(down[v], up[v])
        return res
