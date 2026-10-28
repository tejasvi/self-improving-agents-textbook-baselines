from typing import List
from collections import deque


class Solution:
    def _diameter(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        if n == 1:
            return 0
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        def bfs(src):
            dist = [-1] * n
            dist[src] = 0
            q = deque([src])
            far = src
            while q:
                u = q.popleft()
                if dist[u] > dist[far]:
                    far = u
                for v in adj[u]:
                    if dist[v] < 0:
                        dist[v] = dist[u] + 1
                        q.append(v)
            return far, dist[far]

        far, _ = bfs(0)
        _, d = bfs(far)
        return d

    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        d1 = self._diameter(edges1)
        d2 = self._diameter(edges2)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
