from collections import deque
from typing import List


class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        n = len(positions)
        N = 50
        moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

        def bfs(sx, sy):
            dist = [[-1] * N for _ in range(N)]
            dist[sx][sy] = 0
            q = deque([(sx, sy)])
            while q:
                x, y = q.popleft()
                for dx, dy in moves:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < N and 0 <= ny < N and dist[nx][ny] < 0:
                        dist[nx][ny] = dist[x][y] + 1
                        q.append((nx, ny))
            return dist

        # pts[0..n-1] are pawns, pts[n] is knight start
        pts = [(p[0], p[1]) for p in positions] + [(kx, ky)]
        # D[a][b] = knight distance between points a and b
        D = [[0] * (n + 1) for _ in range(n + 1)]
        for a in range(n + 1):
            d = bfs(*pts[a])
            for b in range(n + 1):
                D[a][b] = d[pts[b][0]][pts[b][1]]

        full = (1 << n) - 1
        # dp[mask][last]: max (Alice to move) / min (Bob to move) future moves,
        # where mask = remaining pawns, last = knight's current point index.
        dp = [None] * (1 << n)
        dp[0] = [0] * (n + 1)
        for mask in range(1, full + 1):
            captured = n - bin(mask).count("1")
            alice = captured % 2 == 0
            if alice:
                best = [-1] * (n + 1)
            else:
                best = [float("inf")] * (n + 1)
            for i in range(n):
                b = 1 << i
                if not mask & b:
                    continue
                prev = dp[mask ^ b]
                if alice:
                    for last in range(n + 1):
                        v = D[last][i] + prev[i]
                        if v > best[last]:
                            best[last] = v
                else:
                    for last in range(n + 1):
                        v = D[last][i] + prev[i]
                        if v < best[last]:
                            best[last] = v
            dp[mask] = best
        return dp[full][n]
