# Palindromic Shortest Path solution

import sys
from collections import deque

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    N = int(data[0].strip())
    matrix = data[1:1+N]

    # Build adjacency structures
    out_by_label = [dict() for _ in range(N)]   # out_by_label[u][c] = list of v where u->v label c
    rev_by_label = [dict() for _ in range(N)]   # rev_by_label[u][c] = list of v where v->u label c
    edge_exists = [[False]*N for _ in range(N)]

    for i in range(N):
        row = matrix[i]
        for j, ch in enumerate(row):
            if ch != '-':
                edge_exists[i][j] = True
                out_by_label[i].setdefault(ch, []).append(j)
                rev_by_label[j].setdefault(ch, []).append(i)

    # Pre‑compute label sets for fast intersection
    out_labels = [set(d.keys()) for d in out_by_label]
    rev_labels = [set(d.keys()) for d in rev_by_label]

    # visited token trick to avoid reallocating N×N array for every BFS
    visited = [[0]*N for _ in range(N)]
    dist = [[0]*N for _ in range(N)]  # reused, values are valid only when visited==token
    token = 1

    ans = [[-1]*N for _ in range(N)]
    for i in range(N):
        ans[i][i] = 0  # empty string is a palindrome

    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            # Direct edge gives palindrome of length 1
            if edge_exists[i][j]:
                ans[i][j] = 1
                continue
            # BFS on product graph (a,b) where we have matched the outer part
            dq = deque()
            token += 1
            visited[i][j] = token
            dist[i][j] = 0
            dq.append((i, j))
            best = -1
            while dq:
                a, b = dq.popleft()
                d = dist[a][b]
                # Even length palindrome: meet at same vertex
                if a == b:
                    best = 2 * d
                    break
                # Odd length palindrome: an edge from a to b closes the palindrome
                if edge_exists[a][b]:
                    best = 2 * d + 1
                    break
                # Expand using matching labels on the outward sides
                common = out_labels[a] & rev_labels[b]
                for c in common:
                    for a2 in out_by_label[a][c]:
                        for b2 in rev_by_label[b][c]:
                            if visited[a2][b2] != token:
                                visited[a2][b2] = token
                                dist[a2][b2] = d + 1
                                dq.append((a2, b2))
            ans[i][j] = best
    # Output
    out_lines = [' '.join(str(ans[i][j]) for j in range(N)) for i in range(N)]
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
