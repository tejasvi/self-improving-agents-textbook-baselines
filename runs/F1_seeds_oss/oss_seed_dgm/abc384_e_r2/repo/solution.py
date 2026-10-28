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
    S = [[0]*W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            S[i][j] = int(next(it))
    # directions
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    visited = [[False]*W for _ in range(H)]
    visited[P][Q] = True
    cur = S[P][Q]
    heap = []
    def add_neighbors(i, j):
        for di, dj in dirs:
            ni, nj = i+di, j+dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                heapq.heappush(heap, (S[ni][nj], ni, nj))
                # mark as pending to avoid pushing duplicates multiple times? We could allow duplicates and check visited on pop.
    add_neighbors(P, Q)
    while heap:
        s, i, j = heap[0]
        # check condition s * X < cur
        if s * X < cur:
            heapq.heappop(heap)
            if visited[i][j]:
                continue
            visited[i][j] = True
            cur += s
            add_neighbors(i, j)
        else:
            break
    print(cur)

if __name__ == "__main__":
    solve()
