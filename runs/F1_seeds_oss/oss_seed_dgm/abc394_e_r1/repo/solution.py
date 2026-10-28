# Write your solution here. Read from stdin, write to stdout.

import sys
from collections import deque

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    N = int(data[0].strip())
    grid = [list(line.strip()) for line in data[1:1+N]]
    # adjacency by character
    out_by_char = [[[] for _ in range(26)] for _ in range(N)]  # out_by_char[u][c] = list of v
    in_by_char = [[[] for _ in range(26)] for _ in range(N)]   # in_by_char[v][c] = list of u
    for i in range(N):
        for j in range(N):
            ch = grid[i][j]
            if ch != '-':
                idx = ord(ch) - ord('a')
                out_by_char[i][idx].append(j)
                in_by_char[j][idx].append(i)
    INF = 10**9
    dist = [[INF]*N for _ in range(N)]
    q = deque()
    # base cases: empty palindrome (i==i) length 0
    for i in range(N):
        dist[i][i] = 0
        q.append((i, i))
    # base cases: single edge palindrome length 1
    for i in range(N):
        for c in range(26):
            for j in out_by_char[i][c]:
                if dist[i][j] > 1:
                    dist[i][j] = 1
                    q.append((i, j))
    # BFS on product graph
    while q:
        a, b = q.popleft()
        cur = dist[a][b]
        # try to prepend/append matching characters
        for c in range(26):
            ins = in_by_char[a][c]
            outs = out_by_char[b][c]
            if not ins or not outs:
                continue
            nd = cur + 2
            for i in ins:
                di = dist[i]
                for j in outs:
                    if di[j] > nd:
                        di[j] = nd
                        q.append((i, j))
    # output
    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            val = dist[i][j]
            row.append(str(-1 if val == INF else val))
        out_lines.append(' '.join(row))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
