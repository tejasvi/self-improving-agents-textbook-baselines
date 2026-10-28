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
    S = [[0]*W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            S[i][j] = int(next(it))
    # initial strength
    cur = S[P][Q]
    visited = [[False]*W for _ in range(H)]
    visited[P][Q] = True
    heap = []
    def push(i, j):
        if 0 <= i < H and 0 <= j < W and not visited[i][j]:
            heapq.heappush(heap, (S[i][j], i, j))
            # mark as in-heap to avoid duplicate pushes later? we will check visited on pop.
    # add initial neighbors
    push(P-1, Q)
    push(P+1, Q)
    push(P, Q-1)
    push(P, Q+1)
    while heap:
        s, i, j = heap[0]  # peek smallest
        # condition: s * X < cur
        if s * X < cur:
            heapq.heappop(heap)
            if visited[i][j]:
                continue
            visited[i][j] = True
            cur += s
            # add its neighbors
            push(i-1, j)
            push(i+1, j)
            push(i, j-1)
            push(i, j+1)
        else:
            break
    print(cur)

if __name__ == "__main__":
    solve()
