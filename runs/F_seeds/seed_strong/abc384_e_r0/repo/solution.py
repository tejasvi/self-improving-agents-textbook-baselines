import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    # Absorbable set is monotone: the greedy closure from the start is the maximum.
    # Keep a min-heap of frontier cells; absorb the smallest while X * s < total.
    total = S[P * W + Q]
    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    heap = []

    def push_neighbors(idx):
        r, c = divmod(idx, W)
        if r > 0 and not visited[idx - W]:
            visited[idx - W] = 1
            heapq.heappush(heap, (S[idx - W], idx - W))
        if r < H - 1 and not visited[idx + W]:
            visited[idx + W] = 1
            heapq.heappush(heap, (S[idx + W], idx + W))
        if c > 0 and not visited[idx - 1]:
            visited[idx - 1] = 1
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if c < W - 1 and not visited[idx + 1]:
            visited[idx + 1] = 1
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if X * s >= total:
            break
        heapq.heappop(heap)
        total += s
        push_neighbors(idx)
    print(total)


main()
