import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]

    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    cur = S[start]
    heap = []

    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not visited[idx - W]:
            heapq.heappush(heap, (S[idx - W], idx - W))
        if i < H - 1 and not visited[idx + W]:
            heapq.heappush(heap, (S[idx + W], idx + W))
        if j > 0 and not visited[idx - 1]:
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if j < W - 1 and not visited[idx + 1]:
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if visited[idx]:
            heapq.heappop(heap)
            continue
        if X * s >= cur:
            break  # smallest frontier slime not absorbable => none are
        heapq.heappop(heap)
        visited[idx] = 1
        cur += s
        push_neighbors(idx)

    print(cur)


main()
