from typing import List


class Solution:
    def timeTaken(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # Cost of entering a node: 1 if odd, 2 if even.
        cost = [1 if i % 2 == 1 else 2 for i in range(n)]

        # BFS order from root 0.
        parent = [-1] * n
        order = [0]
        visited = [False] * n
        visited[0] = True
        for u in order:
            for w in adj[u]:
                if not visited[w]:
                    visited[w] = True
                    parent[w] = u
                    order.append(w)

        # down[v]: max cost of path from v into its subtree (0 if leaf).
        down = [0] * n
        for v in reversed(order):
            p = parent[v]
            if p >= 0:
                val = cost[v] + down[v]
                if val > down[p]:
                    down[p] = val

        # up[v]: max cost of path from v going through parent (0 baseline).
        up = [0] * n
        for p in order:
            # top two child values of p
            best1 = best2 = 0
            best1_child = -1
            for c in adj[p]:
                if c == parent[p]:
                    continue
                val = cost[c] + down[c]
                if val > best1:
                    best2 = best1
                    best1 = val
                    best1_child = c
                elif val > best2:
                    best2 = val
            for c in adj[p]:
                if c == parent[p]:
                    continue
                sib = best2 if c == best1_child else best1
                up[c] = cost[p] + max(up[p], sib)

        return [max(down[v], up[v]) for v in range(n)]
