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
    P = int(next(it)) - 1  # zero based
    Q = int(next(it)) - 1
    S = [[0] * W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            S[i][j] = int(next(it))

    # Directions 4-neighbor
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    visited = [[False]*W for _ in range(H)]
    # start cell is Takahashi's slime
    cur = S[P][Q]
    visited[P][Q] = True
    heap = []
    # add initial frontier
    for di,dj in dirs:
        ni, nj = P+di, Q+dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            heapq.heappush(heap, (S[ni][nj], ni, nj))
            visited[ni][nj] = True  # mark as in heap to avoid multiple pushes

    # Process
    while heap:
        strength, i, j = heap[0]  # peek smallest
        # check condition: strength * X < cur
        if strength * X < cur:
            heapq.heappop(heap)
            cur += strength
            # add its neighbors to heap if not already visited
            for di,dj in dirs:
                ni, nj = i+di, j+dj
                if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                    heapq.heappush(heap, (S[ni][nj], ni, nj))
                    visited[ni][nj] = True
        else:
            # smallest frontier not absorbable, cannot absorb any others
            break
    print(cur)

if __name__ == "__main__":
    solve()
