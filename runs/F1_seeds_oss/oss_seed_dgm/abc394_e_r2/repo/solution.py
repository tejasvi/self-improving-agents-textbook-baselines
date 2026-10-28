# Write your solution here. Read from stdin, write to stdout.
import sys
from collections import deque

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    N = int(data[0].strip())
    rows = data[1:1+N]
    # adjacency lists by character (0-25)
    out = [[[] for _ in range(26)] for _ in range(N)]  # out[u][c] -> list of v
    inn = [[[] for _ in range(26)] for _ in range(N)]  # inn[v][c] -> list of u (u->v with char c)
    edges = []  # list of (u,v,c)
    for i in range(N):
        line = rows[i].strip()
        for j, ch in enumerate(line):
            if ch != '-':
                c = ord(ch) - 97
                out[i][c].append(j)
                inn[j][c].append(i)
                edges.append((i, j, c))
    INF = 10**9
    dist = [[INF] * N for _ in range(N)]
    import heapq
    heap = []
    # base cases: empty palindrome (i==i)
    for i in range(N):
        dist[i][i] = 0
        heapq.heappush(heap, (0, i, i))
    # base case: single edge palindrome (any label) length 1
    for u, v, c in edges:
        if dist[u][v] > 1:
            dist[u][v] = 1
            heapq.heappush(heap, (1, u, v))
    # Dijkstra on state space (i,j) with transitions adding two characters at both ends
    while heap:
        d, a, b = heapq.heappop(heap)
        if d != dist[a][b]:
            continue
        # we want to go to predecessor states (i,j) such that i->a (c) and b->j (c)
        for c in range(26):
            if not inn[a][c] or not out[b][c]:
                continue
            for i in inn[a][c]:
                for j in out[b][c]:
                    nd = d + 2
                    if nd < dist[i][j]:
                        dist[i][j] = nd
                        heapq.heappush(heap, (nd, i, j))
    # output
    out_lines = []
    for i in range(N):
        line = []
        for j in range(N):
            val = dist[i][j]
            if val >= INF:
                line.append('-1')
            else:
                line.append(str(val))
        out_lines.append(' '.join(line))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
