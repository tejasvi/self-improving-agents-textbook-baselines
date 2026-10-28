import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = data[5:5 + H * W]
    grid = [int(v) for v in S]

    absorbed = bytearray(H * W)
    start = P * W + Q
    cur = grid[start]
    absorbed[start] = 1
    heap = []

    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not absorbed[idx - W]:
            heapq.heappush(heap, (grid[idx - W], idx - W))
        if i < H - 1 and not absorbed[idx + W]:
            heapq.heappush(heap, (grid[idx + W], idx + W))
        if j > 0 and not absorbed[idx - 1]:
            heapq.heappush(heap, (grid[idx - 1], idx - 1))
        if j < W - 1 and not absorbed[idx + 1]:
            heapq.heappush(heap, (grid[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if absorbed[idx]:
            heapq.heappop(heap)
            continue
        if X * s < cur:
            heapq.heappop(heap)
            absorbed[idx] = 1
            cur += s
            push_neighbors(idx)
        else:
            break
    print(cur)


main()
