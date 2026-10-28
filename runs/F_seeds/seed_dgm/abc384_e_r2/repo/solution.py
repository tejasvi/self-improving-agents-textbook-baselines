import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    n = H * W
    visited = [False] * n
    start = P * W + Q
    visited[start] = True
    cur = S[start]
    heap = []

    def push_neighbors(idx):
        r, c = divmod(idx, W)
        if r > 0 and not visited[idx - W]:
            heapq.heappush(heap, (S[idx - W], idx - W))
        if r < H - 1 and not visited[idx + W]:
            heapq.heappush(heap, (S[idx + W], idx + W))
        if c > 0 and not visited[idx - 1]:
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if c < W - 1 and not visited[idx + 1]:
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if visited[idx]:
            heapq.heappop(heap)
            continue
        # absorbable iff s < cur / X  <=>  X * s < cur
        if X * s < cur:
            heapq.heappop(heap)
            visited[idx] = True
            cur += s
            push_neighbors(idx)
        else:
            break
    print(cur)


main()
