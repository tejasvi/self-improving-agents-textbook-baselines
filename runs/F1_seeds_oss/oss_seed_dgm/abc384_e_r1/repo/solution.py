# Write your solution here. Read from stdin, write to stdout.
import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1  # 0-indexed
    Q = int(next(it)) - 1
    S = [[0] * W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            S[i][j] = int(next(it))

    # absorbed cells
    absorbed = [[False] * W for _ in range(H)]
    absorbed[P][Q] = True
    cur = S[P][Q]

    # heap of frontier cells (strength, i, j)
    heap = []
    in_heap = [[False] * W for _ in range(H)]
    def push(i, j):
        if 0 <= i < H and 0 <= j < W and not absorbed[i][j] and not in_heap[i][j]:
            heapq.heappush(heap, (S[i][j], i, j))
            in_heap[i][j] = True

    # initial neighbours of starting cell
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        push(P + di, Q + dj)

    # Main loop: always try the smallest strength in frontier.
    while heap:
        strength, i, j = heap[0]
        # condition: strength * X < cur (i.e., strength < cur / X)
        if strength * X < cur:
            heapq.heappop(heap)
            # absorb this slime
            cur += strength
            absorbed[i][j] = True
            # its neighbours may become reachable
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                push(i + di, j + dj)
        else:
            # smallest reachable slime already too strong -> no further absorptions possible
            break

    print(cur)

if __name__ == "__main__":
    solve()
