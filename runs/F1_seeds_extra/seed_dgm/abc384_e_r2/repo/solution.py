import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = data[5:5 + H * W]
    grid = [int(v) for v in S]

    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    strength = grid[start]
    heap = []

    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not visited[idx - W]:
            heapq.heappush(heap, (grid[idx - W], idx - W))
        if i < H - 1 and not visited[idx + W]:
            heapq.heappush(heap, (grid[idx + W], idx + W))
        if j > 0 and not visited[idx - 1]:
            heapq.heappush(heap, (grid[idx - 1], idx - 1))
        if j < W - 1 and not visited[idx + 1]:
            heapq.heappush(heap, (grid[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if visited[idx]:
            heapq.heappop(heap)
            continue
        if X * s >= strength:
            break
        heapq.heappop(heap)
        visited[idx] = 1
        strength += s
        push_neighbors(idx)

    print(strength)


main()
