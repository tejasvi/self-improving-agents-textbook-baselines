# Write your solution here. Read from stdin, write to stdout.

import sys
import heapq

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1
    S = [[int(next(it)) for _ in range(W)] for _ in range(H)]

    visited = [[False] * W for _ in range(H)]
    cur = S[P][Q]
    visited[P][Q] = True
    # frontier min-heap by slime strength
    heap = []
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    def try_push(i, j):
        if 0 <= i < H and 0 <= j < W and not visited[i][j]:
            heapq.heappush(heap, (S[i][j], i, j))
            visited[i][j] = True  # mark as in frontier to avoid duplicates
    # initially add adjacent cells
    for di, dj in dirs:
        try_push(P+di, Q+dj)
    # Use a loop: we may need to consider newly reachable cells after each absorption
    # However, marking visited prematurely blocks re-adding after strength changes.
    # Instead, we keep a separate frontier set.
    # Simpler: use visited for taken cells only, and a separate in_frontier set.
    # Let's rewrite with proper logic.

    # Reset structures for correct algorithm
    visited = [[False] * W for _ in range(H)]
    in_frontier = [[False] * W for _ in range(H)]
    cur = S[P][Q]
    visited[P][Q] = True
    heap = []
    def add(i, j):
        if 0 <= i < H and 0 <= j < W and not visited[i][j] and not in_frontier[i][j]:
            heapq.heappush(heap, (S[i][j], i, j))
            in_frontier[i][j] = True
    for di, dj in dirs:
        add(P+di, Q+dj)
    # Greedy absorption: always take the smallest strength slime that is admissible.
    while heap:
        s, i, j = heap[0]
        # condition: s < cur / X  (i.e., s * X < cur)
        if s * X < cur:
            heapq.heappop(heap)
            # absorb
            cur += s
            visited[i][j] = True
            # add new adjacent cells
            for di, dj in dirs:
                add(i+di, j+dj)
        else:
            break
    print(cur)

if __name__ == "__main__":
    solve()
