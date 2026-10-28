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

        # pts[0] = knight start, pts[1..n] = pawns
        pts = [(kx, ky)] + [(p[0], p[1]) for p in positions]
        # d[a][b] = moves from pts[a] to pawn b (index into positions)
        d = []
        for a in range(n + 1):
            dist = bfs(*pts[a])
            d.append([dist[pts[b + 1][0]][pts[b + 1][1]] for b in range(n)])

        full = (1 << n) - 1
        sys_popcount = [bin(m).count("1") for m in range(1 << n)]

        # f(mask, last): mask = remaining pawns; last = point index (0 = knight start, i+1 = pawn i)
        # Total moves from here on under optimal play.
        memo = {}

        def f(mask, last):
            if mask == 0:
                return 0
            key = mask * (n + 1) + last
            if key in memo:
                return memo[key]
            alice = ((n - sys_popcount[mask]) % 2 == 0)
            best = None
            m = mask
            while m:
                low = m & -m
                i = low.bit_length() - 1
                m ^= low
                val = d[last][i] + f(mask ^ low, i + 1)
                if best is None:
                    best = val
                elif alice:
                    if val > best:
                        best = val
                elif val < best:
                    best = val
            memo[key] = best
            return best

        return f(full, 0)
