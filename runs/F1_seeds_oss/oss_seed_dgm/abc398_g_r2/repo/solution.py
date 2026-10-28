#!/usr/bin/env python3
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    g = [[] for _ in range(N)]
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        g[u].append(v)
        g[v].append(u)
    visited = [False] * N
    color = [0] * N
    forbidden = 0
    for i in range(N):
        if not visited[i]:
            q = deque([i])
            visited[i] = True
            color[i] = 0
            cnt = [0, 0]
            while q:
                v = q.popleft()
                cnt[color[v]] += 1
                for nb in g[v]:
                    if not visited[nb]:
                        visited[nb] = True
                        color[nb] = color[v] ^ 1
                        q.append(nb)
            a, b = cnt
            forbidden += a * (a - 1) // 2 + b * (b - 1) // 2
    total_pairs = N * (N - 1) // 2
    moves = total_pairs - M - forbidden
    if moves & 1:
        sys.stdout.write('Aoki')
    else:
        sys.stdout.write('Takahashi')

if __name__ == "__main__":
    main()
