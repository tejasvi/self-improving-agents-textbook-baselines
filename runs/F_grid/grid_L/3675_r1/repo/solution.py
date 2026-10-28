from typing import List


class Solution:
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        n = len(edges) + 1
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        parent = [-1] * n
        parent_w = [0] * n
        order = []
        visited = [False] * n
        visited[0] = True
        stack = [0]
        while stack:
            u = stack.pop()
            order.append(u)
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    parent_w[v] = w
                    stack.append(v)

        dp0 = [0] * n  # node keeps at most k child edges
        dp1 = [0] * n  # node keeps at most k-1 child edges (edge to parent kept)
        for u in reversed(order):
            base = 0
            gains = []
            for v, w in adj[u]:
                if v == parent[u]:
                    continue
                base += dp0[v]
                g = dp1[v] + w - dp0[v]
                if g > 0:
                    gains.append(g)
            gains.sort(reverse=True)
            dp0[u] = base + sum(gains[:k])
            dp1[u] = base + sum(gains[:k - 1]) if k - 1 > 0 else base

        return dp0[0]
