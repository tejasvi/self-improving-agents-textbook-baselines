# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
    degree = [len(nei) for nei in adj]
    # leaf neighbor count for each node: number of adjacent vertices that are leaves (degree == 1) and are not the node itself.
    leaf_adj = [0] * n
    for v in range(n):
        if degree[v] == 1:  # leaf
            # its only neighbor gains one leaf adjacent
            nb = adj[v][0]
            leaf_adj[nb] += 1
    best_keep = 0
    # For each possible root r, consider its neighbors as potential middle vertices.
    for r in range(n):
        caps = []
        for nb in adj[r]:
            # For neighbor nb, the number of leaf children it can provide (excluding r) is leaf_adj[nb]
            # However, if nb itself is a leaf (degree==1), leaf_adj[nb] == 0, cannot be a middle vertex.
            caps.append(leaf_adj[nb])
        caps.sort(reverse=True)
        # choose i middle vertices (i >= 1) with the smallest leaf count among them being y
        for i, y in enumerate(caps, start=1):
            if y <= 0:
                break  # need positive y
            keep = 1 + i * (y + 1)  # root + i middle vertices + i*y leaves
            if keep > best_keep:
                best_keep = keep
    # answer = deletions
    print(n - best_keep)

if __name__ == "__main__":
    solve()
